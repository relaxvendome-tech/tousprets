package fr.tousprets.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.ActivityNotFoundException
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.print.PrintAttributes
import android.print.PrintManager
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.widget.FrameLayout
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.webkit.WebViewAssetLoader
import androidx.webkit.WebViewClientCompat

/**
 * Tous prêts — appli Android native.
 * Le site est embarqué dans l'APK (assets/site) et servi en https local via
 * WebViewAssetLoader : l'appli fonctionne entièrement hors ligne, sans serveur.
 */
class MainActivity : ComponentActivity() {

    private companion object {
        const val LOCAL_HOST = WebViewAssetLoader.DEFAULT_DOMAIN // appassets.androidplatform.net
        const val SITE_ROOT = "https://$LOCAL_HOST/assets/site/"
        const val START_URL = SITE_ROOT + "index.html"
        const val PUBLIC_HOST = "tousprets.fr"

        // Ponts JS : partage, impression et téléchargement de la sauvegarde (non gérés par WebView)
        const val BRIDGE_JS = """
(function(){
  if (window.__tpBridge) return; window.__tpBridge = true;
  var blobs = {};
  var origCreate = URL.createObjectURL.bind(URL);
  URL.createObjectURL = function(o){ var u = origCreate(o); if (o instanceof Blob) blobs[u] = o; return u; };
  var origClick = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function(){
    var href = this.getAttribute('href') || '';
    if (this.hasAttribute('download') && href.indexOf('blob:') === 0 && blobs[href]) {
      var name = this.getAttribute('download') || 'tous-prets.json';
      var b = blobs[href];
      b.text().then(function(t){ TPAndroid.saveFile(name, b.type || 'application/octet-stream', t); });
      return;
    }
    return origClick.call(this);
  };
  try {
    Object.defineProperty(navigator, 'share', { configurable: true, value: function(d){
      d = d || {};
      TPAndroid.share(d.title || '', d.text || '', d.url || '');
      return Promise.resolve();
    }});
  } catch(e) {}
  window.print = function(){ TPAndroid.print(document.title || 'Tous prets'); };
})();
"""
    }

    private lateinit var webView: WebView
    private var pendingPermission: PermissionRequest? = null
    private var pendingFileContent: String? = null

    private val cameraPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            val req = pendingPermission ?: return@registerForActivityResult
            pendingPermission = null
            if (granted) {
                req.grant(arrayOf(PermissionRequest.RESOURCE_VIDEO_CAPTURE))
            } else {
                req.deny()
                toast(getString(R.string.camera_denied))
            }
        }

    private val createDocument = registerForActivityResult(
        ActivityResultContracts.CreateDocument("application/json")
    ) { uri: Uri? ->
        val content = pendingFileContent
        pendingFileContent = null
        if (uri == null || content == null) return@registerForActivityResult
        try {
            contentResolver.openOutputStream(uri)?.use { it.write(content.toByteArray(Charsets.UTF_8)) }
                ?: throw IllegalStateException("flux nul")
            toast(getString(R.string.saved))
        } catch (e: Exception) {
            toast(getString(R.string.save_failed))
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)

        val root = FrameLayout(this)
        webView = WebView(this)
        root.addView(
            webView,
            FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        )
        setContentView(root)

        // Contenu sous les barres système (edge-to-edge obligatoire en targetSdk 35+)
        ViewCompat.setOnApplyWindowInsetsListener(root) { v, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            WindowInsetsCompat.CONSUMED
        }

        val assetLoader = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true          // localStorage : checklists, stock, voisins
            allowFileAccess = false
            allowContentAccess = false
            mediaPlaybackRequiresUserGesture = false // flux caméra du scan QR
            setSupportMultipleWindows(false)
            setSupportZoom(false)
        }
        webView.addJavascriptInterface(Bridge(), "TPAndroid")

        webView.webViewClient = object : WebViewClientCompat() {
            override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse? =
                assetLoader.shouldInterceptRequest(request.url)

            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean =
                handleUrl(request.url)

            override fun onPageFinished(view: WebView, url: String?) {
                view.evaluateJavascript(BRIDGE_JS, null)
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest) {
                runOnUiThread {
                    val wantsCamera = request.resources.contains(PermissionRequest.RESOURCE_VIDEO_CAPTURE)
                    if (!wantsCamera || request.origin.host != LOCAL_HOST) {
                        request.deny(); return@runOnUiThread
                    }
                    if (ContextCompat.checkSelfPermission(this@MainActivity, Manifest.permission.CAMERA)
                        == PackageManager.PERMISSION_GRANTED
                    ) {
                        request.grant(arrayOf(PermissionRequest.RESOURCE_VIDEO_CAPTURE))
                    } else {
                        pendingPermission?.deny()
                        pendingPermission = request
                        cameraPermission.launch(Manifest.permission.CAMERA)
                    }
                }
            }
        }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) webView.goBack() else finish()
            }
        })

        if (savedInstanceState == null || webView.restoreState(savedInstanceState) == null) {
            webView.loadUrl(START_URL)
        }
    }

    /** true = l'appli gère elle-même l'URL (hors WebView). */
    private fun handleUrl(uri: Uri): Boolean {
        val scheme = uri.scheme?.lowercase()
        val host = uri.host?.lowercase()
        return when {
            host == LOCAL_HOST -> false
            (scheme == "https" || scheme == "http") && (host == PUBLIC_HOST || host == "www.$PUBLIC_HOST") -> {
                // Liens absolus vers le site : on ouvre la copie embarquée
                val path = uri.path?.trimStart('/').orEmpty().ifEmpty { "index.html" }
                val fragment = uri.fragment?.let { "#$it" }.orEmpty()
                webView.loadUrl(SITE_ROOT + path + fragment)
                true
            }
            scheme == "tel" -> launch(Intent(Intent.ACTION_DIAL, uri))
            scheme == "sms" || scheme == "smsto" || scheme == "mailto" -> launch(Intent(Intent.ACTION_SENDTO, uri))
            else -> launch(Intent(Intent.ACTION_VIEW, uri)) // sites externes : navigateur
        }
    }

    private fun launch(intent: Intent): Boolean {
        try {
            startActivity(intent)
        } catch (e: ActivityNotFoundException) {
            toast(getString(R.string.no_app))
        }
        return true
    }

    private fun toast(msg: String) = Toast.makeText(this, msg, Toast.LENGTH_SHORT).show()

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        webView.saveState(outState)
    }

    override fun onDestroy() {
        pendingPermission?.deny()
        webView.destroy()
        super.onDestroy()
    }

    /** Appelé depuis le JS de la page (thread binder → retour sur le thread UI). */
    private inner class Bridge {
        @JavascriptInterface
        fun share(title: String, text: String, url: String) = runOnUiThread {
            val body = listOf(text, url).filter { it.isNotBlank() }.joinToString("\n")
            val send = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_TEXT, body)
                if (title.isNotBlank()) putExtra(Intent.EXTRA_SUBJECT, title)
            }
            launch(Intent.createChooser(send, getString(R.string.share_title)))
        }

        @JavascriptInterface
        fun print(title: String) = runOnUiThread {
            val pm = getSystemService(PRINT_SERVICE) as PrintManager
            val name = title.ifBlank { "Tous prêts" }
            pm.print(name, webView.createPrintDocumentAdapter(name), PrintAttributes.Builder().build())
        }

        @JavascriptInterface
        fun saveFile(name: String, mime: String, content: String) = runOnUiThread {
            pendingFileContent = content
            try {
                createDocument.launch(name.ifBlank { "tous-prets-sauvegarde.json" })
            } catch (e: ActivityNotFoundException) {
                pendingFileContent = null
                toast(getString(R.string.save_failed))
            }
        }
    }
}
