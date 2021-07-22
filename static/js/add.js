let dd = new Date().getDate();
let mm = new Date().getMonth()+1; 
let yyyy = new Date().getFullYear();
if(dd<10)
    dd='0'+dd
if(mm<10)
    mm='0'+mm
let today = yyyy+'-'+mm+'-'+dd;
document.getElementById('date').min=today