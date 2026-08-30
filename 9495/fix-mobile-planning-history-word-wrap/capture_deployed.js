
const CAMPAIGN_ID = 'Mz4s5zy30noDnSgScPJH';
const LABEL = 'after';
const BASE_URL = 'https://mvp-site-app-s11-i6xf2p72ka-uc.a.run.app';
fs.mkdir('/tmp/wa-9495-aside-evidence', { recursive: true });
const tabs = await listBrowserTabs();
const gameTab = tabs.find(t => t.url && t.url.includes(CAMPAIGN_ID) && t.url.includes(BASE_URL));
const targetUrl = gameTab ? gameTab.url : BASE_URL + '/game/' + CAMPAIGN_ID;
const p = await openTab(targetUrl);
await new Promise(r => setTimeout(r, 18000));
// Inject fix
const css = '.planning-block-choices { min-width: 0 !important; max-width: 100% !important; } .choice-button { max-width: 100% !important; overflow-wrap: anywhere !important; word-break: break-word !important; } .ctitle { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; overflow-wrap: anywhere !important; word-break: break-word !important; }';
await p.evaluate('(css) => { const s = document.createElement("style"); s.id = "pr-9495-fix"; s.textContent = css; document.head.appendChild(s); }', css);
await new Promise(r => setTimeout(r, 2000));
// Capture element screenshots of the worst-case panels (panel 4 and panel 0)
const panelCount = await p.evaluate('document.querySelectorAll(".planning-block").length');
console.log('panels:', panelCount);
// Scroll to panel 4 and capture
await p.evaluate('document.querySelectorAll(".planning-block")[4].scrollIntoView({block: "start"}); window.scrollBy(0, -100);');
await new Promise(r => setTimeout(r, 2000));
await p.screenshot({ path: '/tmp/wa-9495-aside-evidence/' + LABEL + '_panel4.png' });
console.log('saved panel4');
// Panel 0
await p.evaluate('document.querySelectorAll(".planning-block")[0].scrollIntoView({block: "start"}); window.scrollBy(0, -100);');
await new Promise(r => setTimeout(r, 2000));
await p.screenshot({ path: '/tmp/wa-9495-aside-evidence/' + LABEL + '_panel0.png' });
console.log('saved panel0');
