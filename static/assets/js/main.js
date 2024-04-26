/*

  Main JavaScript File for Human Sun Folio Template

  Author: Haradhan Sharma
  Date: April 2, 2024
  Version: 1.0

  This is the main JavaScript file for your website. It controls the interactivity and functionality 
  of your web pages. 

  **Dependencies:**  MagicMouse JS, Vivus JS, OverlayScrollbar

*/
$(document).ready(function() {    
    // Print button 
    $('.printButton').on('click', function() {
      window.print(); 
    });
    // print button  

    // go back button      
    $('#goBackButton').click(function() {
        goBack();
      });
    // go back button


    // magic mouse settings start ===============>       
    var mm_options = {
        "outerStyle": "circle",
        "hoverEffect": "pointer-overlay",
        "hoverItemMove": false,
        "defaultCursor": false,
        "outerWidth": 40,
        "outerHeight": 40
    }; 

    //initiate magic ouse
    magicMouse(mm_options); 

    // altering default behacior of magic mouse 
    alterMagicMouse(); 
    
    // applyng magic mouse with different blend mode
    $('.specialeffect').each(function() {
        changeMouseSize($(this), mm_options);
    });  

    // applying magic mouse with pointer blur
    $('.specialeffectImage').each(function() {  
        changeMouseSize($(this), mm_options, "pointer-blur");        
    });
    

    // car effect with magic mouse
    $('.cardeffectEx').each(function() {
        setCardEffectMagicMouse($(this));
    });


    // calling windows loader. ust be after magic mouse
    callLoader();

    // magic mouse settings end ===========>
    

    // Vivus settings ============================>    
    // Call the function for each element ID
    initVivusAnimation('arrow_to_video', 200, 3000);
    initVivusAnimation('pegion', 200, 3000);        
    // Vivus settings ============================>  


    // Overlay JS configuration as per doc 
    var { 
        OverlayScrollbars, 
        ScrollbarsHidingPlugin, 
        SizeObserverPlugin, 
        ClickScrollPlugin  
    } = OverlayScrollbarsGlobal;

    // Initialize OverlayScrollbars for the body
    OverlayScrollbars(document.body, {});  


    // Initialize OverlayScrollbars for the #applyScrolbar element
    var applyScrollbarElement = document.querySelector('#applyScrolbar');
    if (applyScrollbarElement) {
        OverlayScrollbars(applyScrollbarElement, {
            overflow: {
                x: 'hidden',
                y: 'scroll'
            },
        });
    } else {
        console.error('Element with ID "applyScrolbar" not found.');
    }
    // end overlay scroll bar



    // got to top button
    $(window).scroll(function() {
    if ($(this).scrollTop() > 20) {
          $('#goToTopBtn').fadeIn();
        } else {
          $('#goToTopBtn').fadeOut();
        }
    });

    $('#goToTopBtn').click(function() {
        $('html, body').animate({
          scrollTop: 0
        }, 200);
    });
    // go to top button


    // glitbox gallery start. refer to the documentation of glitbox    

    var lightbox1 = GLightbox({
        touchNavigation : true,
        loop : true,
        autoplayVideos : true,
        selector : '.glightbox'
    });
    

    
    // glitbox gallery end    


    // skills marquee =============>
    // Call the function for each container with their respective direction
    // setupMarquee('marqueeContainer', 'left');
    // setupMarquee('marqueeContainer2', 'left');
    // setupMarquee('marqueeContainer3', 'right'); 

        // Skills marquee =============>    
    if (typeof experiences !== 'undefined' && experiences.length > 0) {
        experiences.forEach(function(experience) {
            let exp_pk = experience.pk.toString();
            let skil_dire = experience.fields.skills_marquee_direction.toString();      
            setupMarquee('marqueeContainer' + exp_pk, skil_dire);     
        });
    }
    // skills marquee =============>


    // Explore me section icon animation start
    $(".explore-cards").each(function(){   
        // resetting to the default for background color
        $(this).on('mouseenter', function(){
            $(this).find('.bs-icon').addClass('end-0 bg-danger');
        });
        $(this).on('mouseleave', function(){
            $(this).find('.bs-icon').removeClass('end-0 bg-danger');
        });
    }); 
    // Explore me section icon animation end     

    $('.copy-button').click(function() {
        var textToCopy = $('.copyEl').text().trim();
        copyToClipboard(textToCopy);
    });

    $('.copy-embed-button').click(function() {
        var embedCode = $('.embed-textarea').val().trim();
        copyToClipboard(embedCode);
    });

});

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        var alertMessage = "Copied to clipboard";
        $('.copyalert').text(alertMessage).fadeIn().delay(2000).fadeOut();
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
    });
}

function changeMouseSize(eL, mm_options, hoverEffect = "pointer-overlay") {
    var specialeffect = $(eL);
    var specialeffectWidthHalf = specialeffect.width() / 2;
    var magicPointer = $('body #magicPointer');
    var magicMouseCursor  = $('body #magicMouseCursor');

    // Altering the original size based on eL
    specialeffect.on('mouseenter', function() {
        magicPointer.css({
            width: (specialeffectWidthHalf) + "px",
            height: (specialeffectWidthHalf) + "px"
        });
        magicMouseCursor.css({
            border: "none",
        });
        magicPointer.removeClass(mm_options.hoverEffect);
        magicPointer.addClass(hoverEffect);     

    });

    // Resetting default size and hover effect
    specialeffect.on('mouseleave', function() {
        magicPointer.css({
            width: "",
            height: ""
        });      
        magicMouseCursor.css({
            border: "",
        });
        magicPointer.removeClass(hoverEffect);   
        magicPointer.addClass(mm_options.hoverEffect);  
    });
}

// go back button
function goBack() {
  window.history.back();
}

// loader
function showLoader() {
    $('#main').addClass('hidden');
    $('#loader').removeClass('hidden');
    $('#loader .circle').removeClass('hidden');

}

function hideLoader() {
    $('#main').removeClass('hidden');
    $('#loader').addClass('hidden');
    $('#loader .circle').addClass('hidden');
}

function callLoader() {
    showLoader();
    if (document.readyState === 'complete') {
        hideLoader();
    } else {
        setTimeout(function() {
            hideLoader();
        }, 500);
    }
}
// Loader


function setupMarquee(containerId, direction) {
    const container = $('#' + containerId);
    const items = container.find('.scrolling-content');
    const containerWidth = container.width();

    let originalWidth = 0;
    items.each(function() {
        originalWidth += $(this).outerWidth();
    });

    let totalWidth = 0;

    if (direction === 'left') {
        while (totalWidth < containerWidth) {
            items.each(function() {
                const clone = $(this).clone(true);
                container.append(clone);
                totalWidth += clone.outerWidth();
            });
        }
    } else if (direction === 'right') {
        while (totalWidth < containerWidth) {
            items.each(function() {
                const clone = $(this).clone(true);
                container.prepend(clone);
                totalWidth += clone.outerWidth();
            });
        }
    }

    let scrollPosition = 0;

    function loopMarquee() {
        if (direction === 'left') {
            scrollPosition -= 0.5;
        } else if (direction === 'right') {
            scrollPosition += 0.5;
        }
        
        container.css('transform', `translateX(${scrollPosition}px)`);

        if (direction === 'left' && Math.abs(scrollPosition) >= originalWidth) {
            scrollPosition = 0;
            container.css('transform', `translateX(${scrollPosition}px)`);
        } else if (direction === 'right' && scrollPosition >= originalWidth) {
            scrollPosition = 0;
            container.css('transform', `translateX(${scrollPosition}px)`);
        }
        requestAnimationFrame(loopMarquee);
    }
    loopMarquee();
}

// Vivus SVG animation as per vivus js doc
function initVivusAnimation(elementId, duration, speed) {
    var element = $('#' + elementId);
    if (element.length > 0) {
        new Vivus(elementId, {
            type: 'delayed',
            duration: duration,
            animTimingFunction: Vivus.EASE
        }, function (myVivus) {
            setTimeout(function () {
                myVivus.play(myVivus.getStatus() === 'end' ? -1 : 1);
            }, speed);
        });
    }
}

function alterMagicMouse() {
    const mousePointerTrans = "background 0.5s, width 0.4s, height 0.4s, border-radius 0.4s";
    // altering default pointer
    $('body #magicPointer').css({
        transition : mousePointerTrans,       
        'z-index': '9999999',
    });  
}



// Ading card effect based on magic mouse
function setCardEffectMagicMouse(eL) {   
    var card = eL;
    var mouseHover = false;
    var mousePosition = { x: 0, y: 0 };
    var cardSize = { width: 0, height: 0 };
    var SCALE_X = 4;
    var SCALE_Y = 8;

    card.blur(function() {
        mouseHover = false;
    });

    card.focus(function() {
        mouseHover = true;
    });

    card.mousemove(function(e) {
        if (!mouseHover) return;
        var rect = card[0].getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        mousePosition = { x, y };
        cardSize = {
            width: card[0].offsetWidth || 0,
            height: card[0].offsetHeight || 0,
        };
        card.css({
            'transition': 'transform 0.4s ease', 
            'transform': 'perspective(1000px) rotateX(' + ((mousePosition.y / cardSize.height) * -(SCALE_Y * 2) + SCALE_Y) + 'deg) rotateY(' + ((mousePosition.x / cardSize.width) * (SCALE_X * 2) - SCALE_X) + 'deg) translateZ(10px)'
            });
    });

    card.mouseout(function() {
        mouseHover = false;
        card.css('transform', 'perspective(600px) rotateX(0deg) rotateY(0deg) translateZ(0px)');
    });

    card.mouseover(function() {
        mouseHover = true;
    });
} 


function setupMarquee(containerId, direction) {
    const container = $('#' + containerId);
    const items = container.find('.scrolling-content');
    const containerWidth = container.width();

    let originalWidth = 0;
    items.each(function() {
        originalWidth += $(this).outerWidth();
    });

    let totalWidth = 0;

    if (direction === 'left') {
        while (totalWidth < containerWidth) {
            items.each(function() {
                const clone = $(this).clone(true);
                container.append(clone);
                totalWidth += clone.outerWidth();
            });
        }
    } else if (direction === 'right') {
        while (totalWidth < containerWidth) {
            items.each(function() {
                const clone = $(this).clone(true);
                container.prepend(clone);
                totalWidth += clone.outerWidth();
            });
        }
    }

    let scrollPosition = 0;

    function loopMarquee() {
        if (direction === 'left') {
            scrollPosition -= 0.5;
        } else if (direction === 'right') {
            scrollPosition += 0.5;
        }
        
        container.css('transform', `translateX(${scrollPosition}px)`);

        if (direction === 'left' && Math.abs(scrollPosition) >= originalWidth) {
            scrollPosition = 0;
            container.css('transform', `translateX(${scrollPosition}px)`);
        } else if (direction === 'right' && scrollPosition >= originalWidth) {
            scrollPosition = 0;
            container.css('transform', `translateX(${scrollPosition}px)`);
        }
        requestAnimationFrame(loopMarquee);
    }
    loopMarquee();
}

    

      























// $(document).ready(function() {

//     callLoader();
//     // Print button 

//     $('.printButton').on('click', function() {
//       window.print(); 
//     });

//     // print button        
//     $('#goBackButton').click(function() {
//         goBack();
//       });
//     // go back button


//     // magic mouse settings start ===============>       
//     var mm_options = {
//         "outerStyle": "circle",
//         "hoverEffect": "pointer-overlay",
//         "hoverItemMove": false,
//         "defaultCursor": false,
//         "outerWidth": 40,
//         "outerHeight": 40
//     }; 
//     magicMouse(mm_options); 
//     alterMagicMouse(); 
    
//     $('.specialeffect').each(function() {
//         changeMouseSize($(this), mm_options);
//     });  

    
//     $('.specialeffectImage').each(function() {  
//         changeMouseSize($(this), mm_options, "pointer-blur");
        
//     });

    

    
    
    

//     $('.cardeffectEx').each(function() {
//         setCardEffectMagicMouse($(this));
//     });


    

//     // magic mouse settings end ===========>
    

//     // Vivus settings ============================>        

//     // Call the function for each element ID
//     initVivusAnimation('my_name_logo', 200, 3000);
//     initVivusAnimation('arrow_to_video', 200, 3000);
//     initVivusAnimation('pegion', 200, 3000);        
//     // Vivus settings ============================>    

    


//     // Overlay JS configuration as per doc 
//     var { 
//         OverlayScrollbars, 
//         ScrollbarsHidingPlugin, 
//         SizeObserverPlugin, 
//         ClickScrollPlugin  
//     } = OverlayScrollbarsGlobal;

//     // Initialize OverlayScrollbars for the body
//     OverlayScrollbars(document.body, {});  


//     // Initialize OverlayScrollbars for the #applyScrolbar element
//     var applyScrollbarElement = document.querySelector('#applyScrolbar');
//     if (applyScrollbarElement) {
//         OverlayScrollbars(applyScrollbarElement, {
//             overflow: {
//                 x: 'hidden',
//                 y: 'scroll'
//             },
//         });
//     } else {
//         console.error('Element with ID "applyScrolbar" not found.');
//     }
//     // end overlay scroll bar



//     // got to top button
//     $(window).scroll(function() {
//     if ($(this).scrollTop() > 20) {
//           $('#goToTopBtn').fadeIn();
//         } else {
//           $('#goToTopBtn').fadeOut();
//         }
//     });

//     $('#goToTopBtn').click(function() {
//         $('html, body').animate({
//           scrollTop: 0
//         }, 200);
//     });
//     // go to top button   




//     const lightbox = GLightbox({
//         touchNavigation: true,
//         loop: true,
//         autoplayVideos: true
//     });

//     lightbox.on('open', () => {
//         $('#magicPointer').css({
//             transition: "none",
//             width: "20px",
//             height: "20px"
//         });      
//     });

//     lightbox.on('close', () => {
//         $('#magicPointer').css({
//             transition: mousePointerTrans,
//             width: "",
//             height: ""
//         });      
//     });


    



//     // Skills marquee =============>    
//     if (typeof experiences !== 'undefined' && experiences.length > 0) {
//         experiences.forEach(function(experience) {
//             let exp_pk = experience.pk.toString();
//             let skil_dire = experience.fields.skills_marquee_direction.toString();      
//             setupMarquee('marqueeContainer' + exp_pk, skil_dire);     
//         });
//     }

    


//     // skills marquee =============>

//     // Altering default magic mouse
//     $(".explore-cards").each(function(){   
//         // resetting to the default for background color
//         $(this).on('mouseenter', function(){
//             $(this).find('.bs-icon').addClass('end-0 bg-danger');
//         });
//         $(this).on('mouseleave', function(){
//             $(this).find('.bs-icon').removeClass('end-0 bg-danger');
//         });
//     });      

// });

// function changeMouseSize(eL, mm_options, hoverEffect = "pointer-overlay") {
//     var specialeffect = $(eL);
//     var specialeffectWidthHalf = specialeffect.width() / 2;
//     var magicPointer = $('#magicPointer');
//     var magicMouseCursor  = $('body #magicMouseCursor');

//     // Altering the original size based on eL
//     specialeffect.on('mouseenter', function() {
//         magicPointer.css({
//             width: (specialeffectWidthHalf) + "px",
//             height: (specialeffectWidthHalf) + "px"
//         });

//         magicMouseCursor.css({
//             border: "none",
//         });

//         magicPointer.removeClass(mm_options.hoverEffect);
//         magicPointer.addClass(hoverEffect);        

//     });

//     // Resetting default size and hover effect
//     specialeffect.on('mouseleave', function() {
//         magicPointer.css({
//             width: "",
//             height: ""
//         });
      
//         magicMouseCursor.css({
//             border: "",
//         });
//         magicPointer.removeClass(hoverEffect);   
//         magicPointer.addClass(mm_options.hoverEffect);       

//     });
// }




// // go back button
// function goBack() {
//   window.history.back();
// }



// // loader
// function showLoader() {
//     $('#main').addClass('hidden');
//     $('#loader').removeClass('hidden');
// }

// function hideLoader() {
//     $('#main').removeClass('hidden');
//     $('#loader').addClass('hidden');
// }

// function callLoader() {
//     showLoader();

//     if (document.readyState === 'complete') {
//         hideLoader();
//     } else {
//         setTimeout(function() {
//             hideLoader();
//         }, 2000);
//     }
// }


// // Loader

// // funtion to set random color
// function getRandomColor() {
//     // Loop until a suitable color is generated
//     while (true) {
//       var color = '#';
//       for (var i = 0; i < 6; i++) {
//         color += Math.floor(Math.random() * 16).toString(16);
//       }
      
//       // Check for brightness using a weighted random selection
//       const weights = { '0': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 6, '8': 5, '9': 4, 'A': 3, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1 };
//       let brightness = 0;
//       for (let char of color.substring(1)) {
//         brightness += weights[char];
//       }
    
//       // Adjust threshold to ensure brightness is above a certain value
//       const threshold = 20; // Experiment with different threshold values
//       if (brightness > threshold) {
//         return color;
//       } 
//     }
//   }

// function setupMarquee(containerId, direction) {
//     const container = $('#' + containerId);
//     const items = container.find('.scrolling-content');
//     const containerWidth = container.width();

//     let originalWidth = 0;
//     items.each(function() {
//         originalWidth += $(this).outerWidth();
//     });

//     let totalWidth = 0;

//     if (direction === 'left') {
//         while (totalWidth < containerWidth) {
//             items.each(function() {
//                 const clone = $(this).clone(true);
//                 container.append(clone);
//                 totalWidth += clone.outerWidth();
//             });
//         }
//     } else if (direction === 'right') {
//         while (totalWidth < containerWidth) {
//             items.each(function() {
//                 const clone = $(this).clone(true);
//                 container.prepend(clone);
//                 totalWidth += clone.outerWidth();
//             });
//         }
//     }

//     let scrollPosition = 0;

//     function loopMarquee() {
//         if (direction === 'left') {
//             scrollPosition -= 0.5;
//         } else if (direction === 'right') {
//             scrollPosition += 0.5;
//         }
        
//         container.css('transform', `translateX(${scrollPosition}px)`);

//         if (direction === 'left' && Math.abs(scrollPosition) >= originalWidth) {
//             scrollPosition = 0;
//             container.css('transform', `translateX(${scrollPosition}px)`);
//         } else if (direction === 'right' && scrollPosition >= originalWidth) {
//             scrollPosition = 0;
//             container.css('transform', `translateX(${scrollPosition}px)`);
//         }
//         requestAnimationFrame(loopMarquee);
//     }
//     loopMarquee();
// }

// // Vivus SVG animation as per vivus js doc
// function initVivusAnimation(elementId, duration, speed) {
//     var element = $('#' + elementId);
//     if (element.length > 0) {
//         new Vivus(elementId, {
//             type: 'delayed',
//             duration: duration,
//             animTimingFunction: Vivus.EASE
//         }, function (myVivus) {
//             setTimeout(function () {
//                 myVivus.play(myVivus.getStatus() === 'end' ? -1 : 1);
//             }, speed);
//         });
//     }
// }

// function alterMagicMouse() {

//     const mousePointerTrans = "background 0.5s, width 0.4s, height 0.4s, border-radius 0.4s";

//     // altering default pointer
//     $('#magicPointer').css({
//         transition : mousePointerTrans,       
//         'z-index': '9999999',
//         // 'background' : "var(--bs-secondary)",
//     });    

//     // Altering default magic mouse
//     // $(".magic-hover").each(function(){   
//     //     // resetting to the default for background color
//     //     $(this).on('mouseenter', function(){
//     //         $('#magicPointer').css({
//     //             background : "#fff" ,
//     //             'width' : 40 + 'px',
//     //             'height' : 40 + 'px'
//     //         });               
//     //     });

//     //     // going to the the altering for background
//     //     $(this).on('mouseleave', function(){
//     //         $('#magicPointer').css({
//     //             background : "var(--bs-secondary)" ,
//     //             'width' : '',
//     //             'height' : ''
//     //         });    
            
//     //     });
//     // });

// }



// // Ading card effect based on magic mouse
// function setCardEffectMagicMouse(eL) {   
//     var card = eL;
//     var mouseHover = false;
//     var mousePosition = { x: 0, y: 0 };
//     var cardSize = { width: 0, height: 0 };
//     var SCALE_X = 4;
//     var SCALE_Y = 8;

//     card.blur(function() {
//         mouseHover = false;
//     });

//     card.focus(function() {
//         mouseHover = true;
//     });

//     card.mousemove(function(e) {
//         if (!mouseHover) return;
//         var rect = card[0].getBoundingClientRect();
//         var x = e.clientX - rect.left;
//         var y = e.clientY - rect.top;
//         mousePosition = { x, y };
//         cardSize = {
//             width: card[0].offsetWidth || 0,
//             height: card[0].offsetHeight || 0,
//         };
//         card.css({
//             'transition': 'transform 0.4s ease', 
//             'transform': 'perspective(1000px) rotateX(' + ((mousePosition.y / cardSize.height) * -(SCALE_Y * 2) + SCALE_Y) + 'deg) rotateY(' + ((mousePosition.x / cardSize.width) * (SCALE_X * 2) - SCALE_X) + 'deg) translateZ(10px)'
//             });
//     });

//     card.mouseout(function() {
//         mouseHover = false;
//         card.css('transform', 'perspective(600px) rotateX(0deg) rotateY(0deg) translateZ(0px)');
//     });

//     card.mouseover(function() {
//         mouseHover = true;
//     });
// } 

    

      













