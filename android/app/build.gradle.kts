plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "fr.tousprets.app"
    compileSdk = 36

    defaultConfig {
        // Même nom de paquet que la fiche Play existante
        applicationId = "app.thesurvivaliste.prep"
        minSdk = 24
        targetSdk = 36
        versionCode = 3
        versionName = "2.0.0"
    }

    buildTypes {
        release {
            // Pas de signature ici : l'AAB est signé ensuite avec la clé d'importation
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.activity:activity-ktx:1.10.1")
    implementation("androidx.webkit:webkit:1.14.0")
}
