/* ===== v14 : refonte ergonomique (source : _outils/v14.js, injecté par _outils/v14.py) =====
   - navigation 4 entrées (Accueil, Ma préparation, Bons réflexes, Guides) + historique (bouton retour Android)
   - écran « Ma préparation » : tableau de bord, prochaine action, indispensables, vérification du kit
   - checklist kit 72 h : 3 états (À prévoir / En partie / Disponible), 8 indispensables d'abord,
     catégories repliables, progression sincère
   - foyer : besoins particuliers (bébé, enfants, animaux, personne âgée ou dépendante, traitement)
   Aucune donnée ne quitte l'appareil. Clés ajoutées : tp_needs_v1, tp_kit_check_v1 (sauvegardées),
   tp_last_change_v1, tp_last_backup_v1 (techniques). */
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
function rd(k,f){try{var r=localStorage.getItem(k);if(r===null)return f;var v=JSON.parse(r);return (v===null||v===undefined)?f:v}catch(e){return f}}
function wr(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function fr(n){return String(n).replace('.',',')}
function dateFr(t){try{return new Date(t).toLocaleDateString('fr-FR',{day:'numeric',month:'long',year:'numeric'})}catch(e){return ''}}
function hh(){try{return householdSize()}catch(e){return 1}}

/* ---------- sauvegarde : nouvelles clés, dates ---------- */
try{['tp_needs_v1','tp_kit_check_v1'].forEach(function(k){if(BACKUP_KEYS.indexOf(k)<0)BACKUP_KEYS.push(k)})}catch(e){}
var _save=save;
save=function(k,v){_save(k,v);if(k!=='theme_v1'){try{localStorage.setItem('tp_last_change_v1',JSON.stringify(Date.now()))}catch(e){}}};
var ex=$('exportData');if(ex)ex.addEventListener('click',function(){wr('tp_last_backup_v1',Date.now());setTimeout(renderDash,50)});

/* ---------- navigation ---------- */
var ALL=['home','prep','scenarios','guides','stock','profils','contacts','voisinage'];
var PREP=['prep','scenarios','stock','profils','contacts','voisinage'];
var cur='home';
showScreen=function(name,noPush){
  if(ALL.indexOf(name)<0)name='home';
  if(name!=='voisinage'&&typeof stopNbCamera==='function')stopNbCamera();
  ALL.forEach(function(s){var el=$('screen-'+s);if(el)el.classList.toggle('active',s===name)});
  var tab=PREP.indexOf(name)>=0?'prep':name;
  document.querySelectorAll('nav.bottom [data-screen]').forEach(function(b){var on=b.dataset.screen===tab;b.classList.toggle('active',on);if(on)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current')});
  if(name==='prep')renderDash();
  if(!noPush&&name!==cur){try{history.pushState({tp:name},'',name==='home'?location.pathname+location.search:'#'+(name==='prep'?'ma-preparation':name))}catch(e){}}
  cur=name;
  window.scrollTo({top:0,behavior:'auto'});
  var h=document.querySelector('#screen-'+name+' h2');
  if(h&&name!=='home'){if(!h.hasAttribute('tabindex'))h.setAttribute('tabindex','-1');try{h.focus({preventScroll:true})}catch(e){}}
};
try{history.replaceState({tp:'home'},'')}catch(e){}
window.addEventListener('popstate',function(e){var s=(e.state&&e.state.tp)||'home';showScreen(s,true)});

function go(target,item){
  if(target==='kit'){activeScenario='kit72';showScreen('scenarios');renderScenarioTab();
    if(item){var el=document.querySelector('[data-v14id="'+item+'"]');if(el){el.scrollIntoView({block:'center'});var f=el.querySelector('input:checked')||el.querySelector('input');if(f)try{f.focus({preventScroll:true})}catch(e){}}}
    return}
  if(target==='exercise'){var b=$('exOpen');if(b)b.click();return}
  showScreen(target);
}
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('[data-v14go],a[href="#app-start"],a[href="#ma-preparation"]');
  if(!a)return;
  e.preventDefault();
  go(a.getAttribute('data-v14go')||'prep',a.getAttribute('data-v14item'));
});

/* ---------- états : 0 à prévoir, 1 en partie, 2 disponible ---------- */
function st(v){return (v===true||v===2)?2:((v==='p'||v===1)?1:0)}
var LBL=['À prévoir','En partie','Disponible'];
var HELP=['À ajouter quand vous pourrez.','Une partie est prête.','Prêt et facile à attraper.'];
var EQUIP=[1,2,3,4,5]; /* phases « matériel » du kit 72 h */
var ESS=[
  {id:'1_0',k:'water',n:'Eau potable',q:function(){var h=hh();return (h*6)+' L en bouteilles · 6 L par personne'},a:function(){return 'Mettez de côté '+(hh()*6)+' litres d’eau en bouteilles fermées.'}},
  {id:'1_1',k:'food',n:'Nourriture sans cuisson',q:function(){var h=hh();return '3 jours de repas froids · '+h+' pers.'},a:function(){return 'Rangez quelques conserves qui se mangent froides et un ouvre-boîte.'}},
  {id:'3_1',k:'meds',n:'Médicaments et ordonnances',q:function(){return 'Traitements habituels · copie des ordonnances'},a:function(){return 'Rassemblez vos traitements habituels et une copie des ordonnances.'}},
  {id:'3_0',k:'aid',n:'Trousse de premiers secours',q:function(){return 'Pansements, compresses, désinfectant'},a:function(){return 'Réunissez pansements, compresses et désinfectant dans une boîte.'}},
  {id:'4_0',k:'radio',n:'Radio à piles',q:function(){return 'Avec piles de rechange'},a:function(){return 'Prévoyez une radio à piles ou à manivelle, avec des piles de rechange.'}},
  {id:'2_1',k:'light',n:'Éclairage',q:function(){return 'Lampe de poche ou frontale · piles'},a:function(){return 'Ajoutez une lampe de poche et des piles neuves.'}},
  {id:'5_1',k:'docs',n:'Copies des papiers',q:function(){return 'Dans une pochette étanche'},a:function(){return 'Photocopiez vos papiers importants et glissez-les dans une pochette étanche.'}},
  {id:'5_0',k:'cash',n:'Argent liquide',q:function(){return 'Petites coupures'},a:function(){return 'Gardez quelques billets en petites coupures avec le kit.'}}
];
var ESS_IDS=ESS.map(function(e){return e.id});
function ssv(k){try{return Number(simpleStock[k])||0}catch(e){return 0}}
function stockState(k){
  try{
    if(k==='water'){var o=hh()*6,v=Number(waterStock.val)||0;return v>=o?2:(v>0?1:0)}
    if(k==='food'){var p=parseInt(($('qNourr')||{}).textContent,10)||0;return p>=100?2:(p>0?1:0)}
    var m={meds:'healthBlock_1',aid:'healthBlock_0',radio:'gearBlock_2',light:'gearBlock_1',docs:'gearBlock_14',cash:'gearBlock_3'}[k];
    return m&&ssv(m)>=1?2:0;
  }catch(e){return 0}
}
function essStates(){var c=load(checklistKey('kit72'),{});return ESS.map(function(e){var a=st(c[e.id]),b=stockState(e.k);return {e:e,s:Math.max(a,b),fromStock:b>a}})}

/* besoins particuliers du foyer */
var NEEDS=[
  {k:'baby',n:'Bébé',tip:'Lait infantile prêt à l’emploi, petits pots, couches.',href:'kit-urgence-bebe.html',item:'Lait infantile prêt à l’emploi, petits pots et couches pour 3 jours',src:'Guide officiel'},
  {k:'kids',n:'Enfants',tip:'De quoi les occuper ; parlez-leur du plan de l’école.',href:'kit-urgence-enfants-ecole.html'},
  {k:'pets',n:'Animaux',tip:'Nourriture, eau, laisse ou caisse de transport.',href:'kit-urgence-animaux.html',item:'Nourriture et eau pour l’animal, laisse ou caisse de transport',src:'Guide officiel'},
  {k:'elder',n:'Personne âgée ou dépendante',tip:'Traitements, contacts de l’aidant, registre de la mairie.',href:'kit-urgence-personne-agee.html',item:'Liste des traitements et coordonnées du médecin et de l’aidant',src:'Conseil Tous prêts'},
  {k:'medical',n:'Traitement ou matériel médical',tip:'Prévoyez une solution en cas de coupure de courant, avec votre médecin.',href:'kit-urgence-handicap.html',item:'Matériel médical : solution de secours en cas de coupure (à voir avec votre médecin)',src:'Conseil Tous prêts'}
];
function needs(){var n=rd('tp_needs_v1',{});return (n&&typeof n==='object'&&!Array.isArray(n))?n:{}}

/* ---------- checklist ---------- */
var _rp=renderPhases;
function split(t){var m=String(t).match(/^(.{12,}?)\s(?:\(|:\s|—\s)(.+)$/);if(!m)return [t,''];var d=m[2].replace(/\)\s*$/,'');return [m[1],d]}
function seg(id,v){
  var nm='v14r_'+id.replace(/\W/g,'_');
  return '<div class="v14-seg" role="radiogroup" aria-labelledby="'+nm+'_l">'+[0,1,2].map(function(i){
    return '<label class="v14-s'+i+'"><input type="radio" name="'+nm+'" value="'+i+'"'+(v===i?' checked':'')+'><span>'+LBL[i]+'</span></label>'}).join('')+'</div>';
}
function triRow(id,main,detail,v,extra){
  var nm='v14r_'+id.replace(/\W/g,'_');
  return '<li class="v14-it v14-st'+v+'" data-v14id="'+id+'"><div class="v14-it-t"><span class="v14-it-n" id="'+nm+'_l">'+main+'</span>'
    +(detail?'<span class="v14-it-q">'+detail+'</span>':'')+(extra||'')+'</div>'+seg(id,v)+'</li>';
}
function binRow(scen,id,text,on){
  var p=split(text);
  return '<li class="v14-it v14-bin'+(on?' v14-st2':'')+'" data-v14id="'+id+'"><label class="v14-chk"><input type="checkbox" id="c_'+scen+'_'+id+'"'+(on?' checked':'')+'><span><span class="v14-it-n">'+p[0]+'</span>'+(p[1]?'<span class="v14-it-q">'+p[1]+'</span>':'')+'</span></label></li>';
}
function countTxt(d,t){return d+' / '+t}
function kitStats(c){
  var es=essStates(),ed=0,ep=0;es.forEach(function(x){if(x.s===2)ed++;else if(x.s===1)ep++});
  var tot=0,sum=0;
  SCENARIOS.kit72.phases.forEach(function(ph,p){if(EQUIP.indexOf(p)<0)return;ph.items.forEach(function(_,i){var id=p+'_'+i;tot++;var s=st(c[id]);if(ESS_IDS.indexOf(id)>=0){s=es[ESS_IDS.indexOf(id)].s}sum+=s})});
  return {ed:ed,ep:ep,pct:tot?Math.round(sum*50/tot):0,es:es};
}
function progHtml(c){
  var k=kitStats(c),miss=k.es.filter(function(x){return x.s<2});
  var h='<div class="v14-prog" id="v14KitProg"><p class="v14-prog-t"><span><b>'+k.ed+'</b> indispensable'+(k.ed>1?'s':'')+' sur 8 disponible'+(k.ed>1?'s':'')+'</span>'+(k.ep?'<span>'+k.ep+' en partie</span>':'')+'</p>'
   +'<div class="v14-bar" role="img" aria-label="'+k.ed+' indispensables sur 8 disponibles"><i style="width:'+(k.ed*12.5)+'%"></i><i class="p" style="width:'+(k.ep*12.5)+'%"></i></div>'
   +'<p class="v14-prog-n">Matériel du kit : '+k.pct+' %. '
   +(miss.length?'<strong>Prochaine action :</strong> '+esc(miss[0].e.a()):'<strong>Les 8 indispensables sont prêts.</strong> Vérifiez-les deux fois par an.')+'</p></div>';
  return h;
}
function stepsHtml(){
  return '<ol class="v14-steps" aria-label="Les étapes"><li><a href="#" data-v14go="profils">1. Foyer</a></li><li><a href="#v14Ess">2. Indispensables</a></li><li><a href="#v14More">3. Compléments</a></li><li><a href="#" data-v14go="prep">4. Suivi</a></li></ol>';
}
function foyerHtml(){
  var n=profiles.length,nd=needs(),ks=NEEDS.filter(function(x){return nd[x.k]}).map(function(x){return x.n.toLowerCase()});
  return '<div class="v14-foyer"><span><strong>Foyer :</strong> '+(n?(n+' personne'+(n>1?'s':'')):'non renseigné (calcul pour 1 personne)')+(ks.length?' · '+esc(ks.join(', ')):'')+'</span><a href="#" data-v14go="profils" class="v14-link">Modifier</a></div>';
}
renderPhases=function(container,key,checked){
  var main=container.id==='scenarioContent';
  if(key!=='kit72'){if(main)delete container.dataset.v14;return _rp(container,key,checked)}
  if(main)container.dataset.v14='kit72';
  var es=essStates(),h='';
  if(main)h+=stepsHtml()+foyerHtml()+progHtml(checked);
  h+='<section class="card v14-card" id="v14Ess" aria-labelledby="v14EssT"><h3 class="card-head" id="v14EssT">Les 8 indispensables</h3><ul class="v14-list">';
  es.forEach(function(x){
    var v=st(checked[x.e.id]);
    h+=triRow(x.e.id,x.e.n,x.e.q(),v,x.fromStock?'<span class="v14-it-src">D’après votre stock : '+LBL[x.s].toLowerCase()+'</span>':'');
  });
  h+='</ul></section>';
  var nd=needs(),nl=NEEDS.filter(function(x){return nd[x.k]&&x.item});
  if(nl.length){
    h+='<section class="card v14-card" aria-labelledby="v14NeedT"><h3 class="card-head" id="v14NeedT">Pour votre foyer</h3><ul class="v14-list">';
    nl.forEach(function(x){h+=triRow('n_'+x.k,esc(x.item),'',st(checked['n_'+x.k]),'<span class="v14-it-src">'+x.src+' · <a href="'+x.href+'">en savoir plus</a></span>')});
    h+='</ul></section>';
  }
  h+='<h3 class="v14-sub" id="v14More">Équipements et gestes complémentaires</h3><p class="v14-hint">Ouvrez une catégorie quand vous le souhaitez.</p>';
  SCENARIOS.kit72.phases.forEach(function(ph,p){
    var ids=[],eq=EQUIP.indexOf(p)>=0;
    ph.items.forEach(function(_,i){var id=p+'_'+i;if(ESS_IDS.indexOf(id)<0)ids.push([id,ph.items[i]])});
    if(!ids.length)return;
    var done=ids.filter(function(x){return st(checked[x[0]])===2}).length;
    h+='<details class="card v14-card v14-cat'+(ph.danger?' danger':'')+'"><summary class="card-head"><span>'+ph.title.replace(/^Priorité \d+ — /,'')+'</span><span class="v14-count">'+countTxt(done,ids.length)+'</span></summary><ul class="v14-list">';
    ids.forEach(function(x){var p2=split(x[1]);h+=eq?triRow(x[0],p2[0],p2[1],st(checked[x[0]])):binRow('kit72',x[0],x[1],!!checked[x[0]])});
    h+='</ul></details>';
  });
  var PW=[['e_bank','Batterie externe chargée','Rechargez-la tous les 3 mois'],['e_cables','Câbles et adaptateurs nécessaires','Pour vos téléphones et appareils'],['e_station','Station électrique portable','Facultatif · pour plusieurs appareils'],['e_solar','Panneau solaire compatible avec la station','Facultatif · recharge sans réseau']];
  var pd=PW.filter(function(x){return st(checked[x[0]])===2}).length;
  h+='<details class="card v14-card v14-cat"><summary class="card-head"><span>Autonomie électrique (facultatif)</span><span class="v14-count">'+countTxt(pd,PW.length)+'</span></summary><p class="v14-hint v14-pad">Ne fait pas partie du minimum officiel du kit 72 h. <a href="questions-reponses-kit-urgence.html#courant">Batterie ou station : la différence</a></p><ul class="v14-list">';
  PW.forEach(function(x){h+=triRow(x[0],x[1],x[2],st(checked[x[0]]))});
  h+='</ul></details>';
  container.innerHTML=h;
  container.querySelectorAll('.v14-seg input').forEach(function(inp){
    inp.addEventListener('change',function(){
      var li=inp.closest('.v14-it'),id=li.getAttribute('data-v14id'),v=Number(inp.value);
      if(v===2)checked[id]=true;else if(v===1)checked[id]='p';else delete checked[id];
      li.className=li.className.replace(/v14-st\d/,'v14-st'+v);
      save(checklistKey('kit72'),checked);after(container,checked);
    });
  });
  container.querySelectorAll('.v14-bin input').forEach(function(inp){
    inp.addEventListener('change',function(){
      var li=inp.closest('.v14-it'),id=li.getAttribute('data-v14id');
      if(inp.checked)checked[id]=true;else delete checked[id];
      li.classList.toggle('v14-st2',inp.checked);
      save(checklistKey('kit72'),checked);after(container,checked);
    });
  });
};
function after(container,checked){
  updateDashboard();refreshScenarioChips();
  var p=container.querySelector('#v14KitProg');if(p)p.outerHTML=progHtml(checked);
  container.querySelectorAll('details.v14-cat').forEach(function(d){
    var t=d.querySelectorAll('.v14-it').length,n=d.querySelectorAll('.v14-it.v14-st2').length,c=d.querySelector('.v14-count');if(c)c.textContent=countTxt(n,t)});
}
var _rst=renderScenarioTab;
renderScenarioTab=function(){_rst();if(activeScenario==='kit72'){var i=$('scenarioIntro');if(i)i.innerHTML='Liste du guide officiel « Tous responsables » (SGDSN, 20 novembre 2025), adaptée à votre foyer. À vérifier deux fois par an. <a href="kit-de-survie-72h.html">La liste détaillée</a>'}};
scenarioProgress=function(key){
  var c=load(checklistKey(key),{}),t=0,d=0;
  SCENARIOS[key].phases.forEach(function(ph,p){ph.items.forEach(function(_,i){t++;d+=st(c[p+'_'+i])/2})});
  return t?d/t:0;
};

/* ---------- tableau de bord ---------- */
var _ud=updateDashboard;
updateDashboard=function(){_ud();try{honestScore();renderDash();labelSteppers()}catch(e){if(window.console)console.error(e)}};
var lastScore=0;
function honestScore(){
  var raw=0,hon=0,t=0;
  Object.keys(SCENARIOS).forEach(function(key){var c=load(checklistKey(key),{});SCENARIOS[key].phases.forEach(function(ph,p){ph.items.forEach(function(_,i){t++;var v=c[p+'_'+i];if(v)raw++;hon+=st(v)/2})})});
  var el=$('scorePct'),bar=$('scoreBar');if(!el)return;
  var s=parseInt(el.textContent,10)||0;
  if(t)s=Math.round(s-25*(raw-hon)/t);
  var ed=essStates().filter(function(x){return x.s===2}).length;
  if(ed<8)s=Math.min(s,99);
  s=Math.max(0,Math.min(100,s));lastScore=s;
  el.textContent=s+' %';if(bar)bar.style.width=s+'%';
}
function level(s,ed){
  if(s<=0)return ['À commencer','Un premier pas suffit pour démarrer.'];
  if(ed===8&&s>=100)return ['Prêt','Votre préparation est complète. Pensez à la vérifier.'];
  if(s>=80||ed===8)return ['Presque prêt',ed<8?'Il reste '+(8-ed)+' indispensable'+(8-ed>1?'s':'')+' à compléter, sans pression.':'Quelques compléments, à votre rythme.'];
  if(s>=40)return ['En progrès','Votre kit prend forme, continuez à votre rythme.'];
  return ['Premiers pas','Vous posez déjà une base utile.'];
}
function nextAction(es){
  if(!profiles.length)return {t:'Indiquez combien de personnes vivent chez vous.',s:'Les quantités d’eau et de nourriture se calculent toutes seules.',b:'Renseigner mon foyer',go:'profils'};
  var m=es.filter(function(x){return x.s<2})[0];
  if(m)return {t:m.e.a(),s:m.e.n+' · '+m.e.q(),b:'Ouvrir ma checklist',go:'kit',item:m.e.id};
  var ok=false;try{ok=contacts.some(function(c){return String(c.name||'').trim()&&String(c.phone||'').trim()})}catch(e){}
  if(!ok)return {t:'Enregistrez le numéro d’un proche à prévenir.',s:'Il reste sur votre appareil.',b:'Ajouter un contact',go:'contacts'};
  var kc=rd('tp_kit_check_v1',null),d=kc&&kc.d;
  if(!d||Date.now()-d>182*864e5)return {t:'Vérifiez votre kit : dates, piles, eau.',s:'Le guide officiel conseille de le faire deux fois par an.',b:'Ouvrir ma checklist',go:'kit'};
  return {t:'Complétez les équipements complémentaires.',s:'Couverture de survie, chargeur, double des clés…',b:'Voir les compléments',go:'kit'};
}
function renderDash(){
  var box=$('v14Dash');if(!box)return;
  var es=essStates(),ed=es.filter(function(x){return x.s===2}).length,ep=es.filter(function(x){return x.s===1}).length;
  var lv=level(lastScore,ed),na=nextAction(es);
  var nd=needs(),nl=NEEDS.filter(function(x){return nd[x.k]});
  var kc=rd('tp_kit_check_v1',null),lc=rd('tp_last_change_v1',null),lb=rd('tp_last_backup_v1',null);
  var nextCheck=kc&&kc.d?kc.d+182*864e5:null;
  var h='<p class="v14-level"><strong>'+lv[0]+'</strong> · '+lv[1]+'</p>'
   +'<div class="v14-next"><p class="v14-next-k">Prochaine action</p><p class="v14-next-t">'+esc(na.t)+'</p><p class="v14-next-s">'+esc(na.s)+'</p>'
   +'<button type="button" class="btn-primary v14-next-b" data-v14go="'+na.go+'"'+(na.item?' data-v14item="'+na.item+'"':'')+'>'+na.b+'</button></div>'
   +'<h3 class="v14-h3">Les 8 indispensables <span>'+ed+' / 8'+(ep?' · '+ep+' en partie':'')+'</span></h3><ul class="v14-ess" role="list">';
  es.forEach(function(x){h+='<li><button type="button" class="v14-pill v14-st'+x.s+'" data-v14go="kit" data-v14item="'+x.e.id+'"><span class="v14-dot" aria-hidden="true"></span>'+x.e.n+'<span class="v14-sr"> : '+LBL[x.s]+'</span></button></li>'});
  h+='</ul><dl class="v14-meta">'
   +'<div><dt>Besoins du foyer</dt><dd>'+(nl.length?nl.map(function(x){return '<a href="'+x.href+'">'+x.n+'</a>'}).join(', '):'Aucun indiqué · <a href="#" data-v14go="profils">préciser</a>')+'</dd></div>'
   +'<div><dt>Enregistrement</dt><dd>'+(lc?'Automatique, le '+dateFr(lc)+', sur cet appareil':'Automatique, sur cet appareil')+'</dd></div>'
   +'<div><dt>Dernière sauvegarde (fichier)</dt><dd>'+(lb?dateFr(lb):'Jamais')+' · <a href="#" id="v14Bk">Sauvegarder</a></dd></div>'
   +'<div><dt>Prochaine vérification du kit</dt><dd>'+(nextCheck?(nextCheck<Date.now()?'À faire maintenant':dateFr(nextCheck)):'Pas encore planifiée')+' · <a href="#" id="v14Chk">J’ai vérifié mon kit aujourd’hui</a></dd></div>'
   +'</dl>';
  box.innerHTML=h;
  var bk=$('v14Bk');if(bk)bk.addEventListener('click',function(e){e.preventDefault();var b=$('exportData');if(b)b.click()});
  var ck=$('v14Chk');if(ck)ck.addEventListener('click',function(e){e.preventDefault();wr('tp_kit_check_v1',{d:Date.now()});renderDash();var s=$('v14Live');if(s)s.textContent='Vérification enregistrée. Prochaine dans six mois.'});
}
function labelSteppers(){
  document.querySelectorAll('#screen-stock .stepper button').forEach(function(b){
    if(b.hasAttribute('aria-label'))return;var it=b.closest('.inv-item'),n=it&&it.querySelector('.name');var nm=n?n.textContent.trim():'';
    b.setAttribute('aria-label',(b.dataset.act==='inc'?'Ajouter : ':'Retirer : ')+nm)});
}

/* ---------- foyer : besoins particuliers ---------- */
function renderNeeds(){
  var box=$('v14Needs');if(!box)return;var nd=needs();
  box.innerHTML=NEEDS.map(function(x){return '<label class="v14-need"><input type="checkbox" value="'+x.k+'"'+(nd[x.k]?' checked':'')+'><span>'+x.n+'</span></label>'}).join('');
  var tips=$('v14NeedTips');
  function tip(){var n=needs(),l=NEEDS.filter(function(x){return n[x.k]});tips.innerHTML=l.length?'<ul>'+l.map(function(x){return '<li><strong>'+x.n+' :</strong> '+x.tip+' <a href="'+x.href+'">Le guide</a></li>'}).join('')+'</ul>':''}
  box.querySelectorAll('input').forEach(function(i){i.addEventListener('change',function(){var n=needs();if(i.checked)n[i.value]=true;else delete n[i.value];save('tp_needs_v1',n);tip();renderDash();if(activeScenario==='kit72')renderScenarioTab()})});
  tip();
}

/* ---------- démarrage ---------- */
renderNeeds();
renderScenarioTab();
updateDashboard();
function fromHash(){var hs=location.hash.replace('#screen-','#');
  if(hs==='#app-start'||hs==='#ma-preparation'||hs==='#prep')showScreen('prep',true);
  else if(['#stock','#profils','#contacts','#voisinage','#scenarios','#guides'].indexOf(hs)>=0)showScreen(hs.slice(1),true);}
fromHash();window.addEventListener('hashchange',fromHash);
})();
/* /v14 */
