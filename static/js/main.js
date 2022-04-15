/**
* Template Name: Personal - v4.5.0
* Template URL: https://bootstrapmade.com/personal-free-resume-bootstrap-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/


(function() {
 
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)

    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
  
  
 


  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '#navbar .nav-link', function(e) {
    let section = select(this.hash)
    if (section) {
      e.preventDefault()

      

      let navbar = select('#navbar')
      let header = select('#header')
      let sections = select('section', true)
      let navlinks = select('#navbar .nav-link', true)

      navlinks.forEach((item) => {
        item.classList.remove('active')
      })

      this.classList.add('active')

      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }

      if (this.hash == '#header') {
        header.classList.remove('header-top')

       
        let flip_hide = select('.flip_hide', true)
        flip_hide.forEach((item) => {
          item.classList.remove('flip_hide')
        })
        
        sections.forEach((item) => {
          item.classList.remove('section-show')
        })
        return;
      }

      if (!header.classList.contains('header-top')) {
        header.classList.add('header-top')
       
        let flip = select('.cards', true)
        flip.forEach((item) => {
          item.classList.add('flip_hide')
        })
        
        
        setTimeout(function() {
          sections.forEach((item) => {
            item.classList.remove('section-show')
          })
          section.classList.add('section-show')

        }, 350);
      } else {
        sections.forEach((item) => {
          item.classList.remove('section-show')
        })
        section.classList.add('section-show')
      }

      scrollto(this.hash)
      

    }
  }, true)

  /**
   * Activate/show sections on load with hash links
   */
  window.addEventListener('load', () => {     
    
    if (window.location.pathname ) {
      var nlink =  select('#navbar .nav-link', true)
      nlink.forEach((itm) => {
        if (itm.getAttribute('href') == window.location.pathname ) {            
          itm.classList.add('active')                
        } else {
          itm.classList.remove('active')
        }
      });
    }

    if (window.location.hash ) {

      let initial_nav = select(window.location.hash)     

      if (initial_nav) {
        let header = select('#header')
        let navlinks = select('#navbar .nav-link', true) 

        header.classList.add('header-top')
        let head_top = select('.header-top')
        if(head_top){
        select('.showhide').classList.add('flip_hide')
        
      }

     

        navlinks.forEach((item) => {
          if (item.getAttribute('href') == window.location.hash ) {            
            item.classList.add('active')           
          } else {
            item.classList.remove('active')
          }
        })

        

        setTimeout(function() {
          initial_nav.classList.add('section-show')
        }, 350);

        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Skills animation
   */
  let skilsContent = select('.skills-content');
  if (skilsContent) {
    new Waypoint({
      element: skilsContent,
      offset: '80%',
      handler: function(direction) {
        let progress = select('.progress .progress-bar', true);
        progress.forEach((el) => {
          el.style.width = el.getAttribute('aria-valuenow') + '%'
        });
      }
    })
  }

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },

      1200: {
        slidesPerView: 3,
        spaceBetween: 20
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {  
      let pfitem = select('.extrac', true);  
      pfitem.forEach(function(itm) {
        itm.classList.add('flip_hide');        
      }); 

      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'        
      });
      let portfolioFilters = select('#portfolio-flters li', true);
      
      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();   

        let pfitemm = select('.flip_hide', true);        
        pfitemm.forEach(function(itmm) {
          itmm.classList.remove('flip_hide');         
        });         
        portfolioFilters.forEach(function(el) {          
          el.classList.remove('filter-active');          
        });
        this.classList.add('filter-active');

        var df = this.getAttribute('data-filter');
        
        if (df == '*' ){ 
          
          location.reload(true, scrollto)   
          
          

        }else{
          portfolioIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
        }        
      }, true);


      
    }
  });



})()