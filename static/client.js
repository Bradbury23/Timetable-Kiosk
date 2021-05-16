   //Global variables

   const urlRedirect = window.location.origin; 
   
   //changes wallpaper every 50 minutes.
    const background = [
      //Please, add your wallpapers here. 
      "static/images/wallpapers/wallpaper1.jpg",
      "static/images/wallpapers/wallpaper2.jpg",
      "static/images/wallpapers/wallpaper3.jpg",
      "static/images/wallpapers/wallpaper4.jpg",
      "static/images/wallpapers/wallpaper5.jpg",
      "static/images/wallpapers/wallpaper6.jpg",
      "static/images/wallpapers/wallpaper7.jpg"
    ]
     
     const node = document.getElementById("background");
     
     const cycleImages = (images, container, step) => {
         images.forEach((image, index) => (
           setTimeout(() => {
             container.style.backgroundImage = `url(${image})`  
         }, step * (index + 1))
       ))
       setTimeout(() => cycleImages(images, container, step), step * images.length)
      }
     
     cycleImages(background, node, 900000)

   //Displays clock and today's date.
   function startDatetime() {
    //clock 
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById("clock").innerHTML =
    h + ":" + m + ":" + s;
    var t = setTimeout(startDatetime, 500);
    //date
    var d = String(today.getDate()).padStart(2, '0');
    var m = String(today.getMonth() + 1).padStart(2, '0');  
    var y = today.getFullYear();
    document.getElementById("date").innerHTML = 
    today = d + '/' + m + '/' + y;
  }
  
  //This function works in conjunction with the clock component of startDatetime.
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // adds zero in front of numbers < 10.
    return i;
  }

  //Shows loading circle after clicking submit button on /login (index.html). 
  function loading() {
    document.getElementById("loading").style.display = "block";
  }    

  //Prints username, timetable and logs user out.
  function printContent(table){
    var printTable = document.getElementById(table).innerHTML;
    document.body.innerHTML = printTable;
    window.print();
    location.replace(urlRedirect + "/print")
  } 