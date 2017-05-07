window.onresize = (e) => {
  var m1 = document.getElementById("menu1");
  var m2 = document.getElementById("menu2");
  if(window.innerWidth < 1180) {
    m1.style.display = "none";
    m2.style.display = "block";
  }else{
    m1.style.display = "block";
    m2.style.display = "none";
  }
}

window.onresize();
