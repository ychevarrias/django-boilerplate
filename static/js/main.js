let sideBar = document.querySelector("aside.sidebar");
let btnOpenSidebar = document.querySelector("#open-sidebar-btn");
let btnCloseSidebar = document.querySelector("#close-sidebar-btn");

function activeCurrentLink(){
  let currentLink = document.querySelector(`.sidebar a[href='${window.location.pathname}']`);
  if(!currentLink){return null}
  function activate(aEleme){
    aEleme.classList.add("opened");
    let megamenu = aEleme.closest("ul");
    console.log("evaluando", aEleme, megamenu)
    if(megamenu.classList.contains("root")){return null}
    megamenu.classList.remove("h-0")
    let parentLink = megamenu.previousElementSibling;
    if(parentLink.classList.contains("link")){
      parentLink.classList.add("opened");
      activate(parentLink)
    }
    console.log("aEleme.click() -> ", aEleme)
    return null;
  }
  activate(currentLink)
}
activeCurrentLink()
sideBar.addEventListener("click", function(event){
  let target = event.target;
  if(target.nodeName !== 'A'){return null;}
  if(target.href.indexOf("#") !== -1){
    event.preventDefault();
    target.classList.toggle("opened");
    function normalizarHeight(_submenu, _heigth){
      let backwardComplete = false;
      let current = _submenu;
      let level = 0;
      while(!backwardComplete){
        level += 1
        let parentBlock = current.closest("li");
        if(!parentBlock){break;}
        current = parentBlock.closest("ul");
        if(current.classList.contains('root')){backwardComplete=true; break;}
        let newParentHeight = current.offsetHeight + _heigth;
        current.style.height = `${newParentHeight}px`;
      }
    }
    let submenu = target.nextElementSibling;
    if(!submenu){console.warn("No next menú");return null;}
    let hMenu = 0;
    submenu.childNodes.forEach(liEleme => {
      if(liEleme.nodeName !== 'LI'){return null;}
      hMenu += liEleme.offsetHeight;
    });
    if(!submenu.classList.contains("h-0")){
      submenu.style.height = '0px';
      submenu.classList.add("h-0");
      submenu.classList.remove("border-t");
      normalizarHeight(submenu,hMenu * -1)
      return null;
    }
    submenu.classList.add("border-t")
    submenu.style.height = `${hMenu}px`;
    submenu.classList.remove("h-0");
    normalizarHeight(submenu, hMenu)
  }
});

btnOpenSidebar.addEventListener("click", function (event){
  event.preventDefault();
  let overlay = document.querySelector("body > .overlay");
  sideBar.classList.remove("-ml-64");
  overlay.classList.remove("hidden");
  btnCloseSidebar.classList.remove("hidden")
});

btnCloseSidebar.addEventListener("click", function (event){
  event.preventDefault();
  let overlay = document.querySelector("body > .overlay");
  sideBar.classList.add("-ml-64");
  overlay.classList.add("hidden");
  btnCloseSidebar.classList.add("hidden")
});
