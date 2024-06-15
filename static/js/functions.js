//Get the button
var mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}



// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


// show the selected word
window.addEventListener('hashchange', function() {
    var hash = window.location.hash;
    var tabNumber = hash.split('-')[0][2];
    console.log(tabNumber)
    console.log(hash,hash.split('-'))
    var tabPane = document.getElementById('compared' + tabNumber);
    if (tabNumber>= '0' && tabNumber <= '9' &&  tabPane) {
        var tabPanes = document.querySelectorAll('.compared-content');
        for (var i = 0; i < tabPanes.length; i++) {
            tabPanes[i].style.display = 'none';
        }
        tabPane.style.display = 'block';
    }else{
        console.log('else')
        var tabPanes = document.querySelectorAll('.compared-content');

        for (var i = 0; i < tabPanes.length; i++) {
            tabPanes[i].style.display = 'none';
        }
        var hash = window.location.hash.substring(1);
        var tabPane = document.getElementById(hash);
        
        if (tabPane) {
            tabPane.style.display = 'block';
        } else {
            console.error('Tab not found for hash:', hash);
        }
    }
});
    
    
function updateValue(val) {
  document.getElementById('rangeValue').innerText = val;
}


function dropHandler1(ev) {
    ev.preventDefault();
    if (ev.dataTransfer.items) {
        for (var i = 0; i < ev.dataTransfer.items.length; i++) {
            if (ev.dataTransfer.items[i].kind === 'file') {
                var file = ev.dataTransfer.items[i].getAsFile();
                console.log('... file[' + i + '].name = ' + file.name);
                document.getElementById('file1').files = ev.dataTransfer.files;
            }
        }
    } else {
        for (var i = 0; i < ev.dataTransfer.files.length; i++) {
            console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
            document.getElementById('file1').files = ev.dataTransfer.files;
        }
    } 
}

function dropHandler2(ev) {
    ev.preventDefault();
    if (ev.dataTransfer.items) {
        for (var i = 0; i < ev.dataTransfer.items.length; i++) {
            if (ev.dataTransfer.items[i].kind === 'file') {
                var file = ev.dataTransfer.items[i].getAsFile();
                document.getElementById('file2').files = ev.dataTransfer.files;
            }
        }
    } else {
        for (var i = 0; i < ev.dataTransfer.files.length; i++) {
            document.getElementById('file2').files = ev.dataTransfer.files;
        }
    } 
}

function dragOverHandler(ev) {
    ev.preventDefault();
}
