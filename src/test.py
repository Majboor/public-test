import os
import subprocess

class WebLink:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.folder_path = os.path.join('../www/apps', self.folder_name)
        self.file_path = os.path.join(self.folder_path, 'file.html')
    
    def create_folder(self):
        # Check if the folder already exists
        if not os.path.exists(self.folder_path):
            # If not, create it
            os.makedirs(self.folder_path)
            print(f"Folder '{self.folder_name}' created successfully.")
        else:
            print(f"Folder '{self.folder_name}' already exists.")
    
    def create_file_with_data(self, data):
        with open(self.file_path, 'w') as file:
            file.write(data)
        print(f"File 'file.html' created successfully with data in folder '{self.folder_name}'.")
    
    def insert_article_below_comment(self, comment, article_content):
        with open(self.file_path, 'r') as file:
            html_content = file.read()
        
        # Find the index of the comment in the HTML content
        comment_index = html_content.find(comment)
        
        # If the comment exists, insert the article content below it
        if comment_index != -1:
            modified_content = html_content[:comment_index + len(comment)] + article_content + html_content[comment_index + len(comment):]
            with open(self.file_path, 'w') as file:
                file.write(modified_content)
            print("Article inserted successfully below the comment.")
        else:
            print("Comment not found. Article not inserted.")
        
        return self.file_path
    
    def add_header(self, header_content):
        with open(self.file_path, 'r') as file:
            html_content = file.read()
        
        # Find the index of the header comment
        header_comment_index = html_content.find("<!-- add header below -->")
        
        # If the header comment exists, insert the header content below it
        if header_comment_index != -1:
            modified_content = html_content[:header_comment_index + len("<!-- add header below -->")] + header_content + html_content[header_comment_index + len("<!-- add header below -->"):]
            with open(self.file_path, 'w') as file:
                file.write(modified_content)
            print("Header added successfully.")
        else:
            print("Header comment not found. Header not added.")
        
        return self.file_path

file_content = """
<!DOCTYPE html>
<html lang="en">

<head>
  <title>Doc</title>

  <!-- Meta -->
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Google Font -->
  <link href="https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700&display=swap" rel="stylesheet">

  <!-- Theme CSS -->
  <link rel="stylesheet" href="./css/style.css">
</head>

<body class="docs-page" data-bs-spy="scroll" data-bs-target="#docs-nav" data-bs-root-margin="-100px 0px -40%">
  <header class="header fixed-top">
    <div class="branding docs-branding">
      <div class="container-fluid position-relative py-2">
        <div class="docs-logo-wrapper gap-2 d-flex">
          <button id="docs-sidebar-toggler" class="docs-sidebar-toggler docs-sidebar-visible d-xl-none" type="button">
            <span></span>
            <span></span>
            <span></span>
          </button>
          <div class="site-logo">
            <a class="navbar-brand" href="index.html">
              <span class="logo-text">Doc <span class="text-alt">Doc</span></span>
            </a>
            <span class="badge bg-primary"></span>
          </div>
        </div>
        
        <div class="docs-top-utilities d-flex justify-content-end align-items-center gap-3">
          <div class="top-search-box d-none d-lg-flex">
            <form class="search-form">
              <input type="search" placeholder="Search the docs..." name="search" class="form-control search-input" autocomplete="off">
              <div id="results"></div>
            </form>
          </div>

          <button type="button" class="btn-changelog btn btn-primary d-none d-lg-flex" data-bs-toggle="modal" data-bs-target="#changelogModal">
            Changelog
          </button>
        </div>
      </div>
    </div>
  </header>

  <div class="docs-wrapper">
<!-- nav here -->
<div id="docs-sidebar" class="docs-sidebar">
  <div class="top-search-box d-lg-none p-3">
  <form class="search-form">
  <input type="text" placeholder="Search the docs..." name="search" class="form-control search-input">
  <button type="submit" class="btn search-btn" value="Search">
  <i class="fas fa-search"></i>
  </button>
  </form>
  </div>
  <nav id="docs-nav" class="docs-nav navbar">
  <ul class="section-items list-unstyled nav flex-column pb-3">
      <!-- Navigation links will be inserted here dynamically -->
  </ul>
  </nav>
  </div>
  <!-- nav end -->

    <div class="docs-content">
      <div class="container">
<!-- add header below -->
<!-- add article below -->
    
        </article>
    
        <footer class="footer">
          <div class="container text-center py-5">
            <!--/* This template is free as long as you keep the footer attribution link. If you'd like to use the template without the attribution link, you can buy the commercial license via our website: themes.3rdwavemedia.com Thank you for your support. :) */-->
            <small class="copyright">Designed with ❤️ by
              <a class="theme-link" href="http://themes.3rdwavemedia.com" target="_blank">Xiaoying Riley</a>
              for developers <br><br> Modified with 🔥 by <a class="theme-link" href="https://github.com/joelthorner" target="_blank">joelthorner</a> for developers</small>
          </div>
        </footer>
      </div>
    </div>
    
  </div>
  <!--docs-wrapper-->

  <!-- Modal -->
  <div class="modal fade" id="changelogModal" tabindex="-1" aria-labelledby="changelogModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title px-3 py-1" id="changelogModalLabel">Changelog</h4>
            <button type="button" class="btn-close p-4" data-bs-dismiss="modal" aria-label="Close">
            </button>
          </div>
          <div class="modal-body">
            <div class="container">
              <div class="row justify-content-center">
                <div class="col-12">
                  <h6 class="mt-3"> <span class="p-2"> Version 1.0.0</span> - 29/06/2021</h6>
                  <ul class="mt-3 mb-5">
                    <li class="ms-3">Lorem ipsum dolor sit amet</li>
                    <li class="ms-3">Lorem ipsum dolor sit amet</li>
                    <ul>
                      <li class="ms-3">Lorem ipsum dolor sit amet</li>
                      <li class="ms-3">Lorem ipsum dolor sit amet</li>
                      <li class="ms-3">Lorem ipsum dolor sit amet</li>
                    </ul>
                    <li class="ms-3">Lorem ipsum dolor sit amet</li>
                  </ul>
                </div>
                <!--end col-->
              </div>
              <!--end row-->
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
    </div>
  </div>


<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">

<!-- Optional theme -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://raw.githubusercontent.com/fat/zoom.js/gh-pages/dist/zoom.min.js"></script>


<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css">

<!-- Latest Highlight.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>

<!-- Initialize Highlight.js -->
<script>hljs.initHighlightingOnLoad();</script>

  <!-- Add hljs languages -->
  <script>
    /*! `json` grammar compiled for Highlight.js 11.6.0 */
    (()=>{var e=(()=>{"use strict";return e=>{const a=["true","false","null"],n={
    scope:"literal",beginKeywords:a.join(" ")};return{name:"JSON",keywords:{
    literal:a},contains:[{className:"attr",begin:/"(\\.|[^\\"\r\n])*"(?=\s*:)/,
    relevance:1.01},{match:/[{}[\],:]/,className:"punctuation",relevance:0
    },e.QUOTE_STRING_MODE,n,e.C_NUMBER_MODE,e.C_LINE_COMMENT_MODE,e.C_BLOCK_COMMENT_MODE],
    illegal:"\\S"}}})();hljs.registerLanguage("json",e)})();

    hljs.highlightAll();
  </script>
  <!-- Shop js -->
  <script>
    const getCookie = (name) => {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim().split('=');
        if (c[0] === name) {
          return c[1];
        }
      }
      return "";
    }

    const setCookie = (name, value, days, path, domain, secure) => {
      let cookie = `${name}=${encodeURIComponent(value)}`;

      // Add expiry date
      if (days) {
        const expiry = new Date();
        expiry.setDate(expiry.getDate() + days);
        cookie += `; expires=${expiry.toUTCString()}`;
      }

      // Add Path, Domain, and Secure
      if (path) cookie += `; path=${path}`;
      if (domain) cookie += `; domain=${domain}`;
      if (secure) cookie += `; secure`;

      // Set an HTTP cookie
      document.cookie = cookie;
    };

    var hasLogin = getCookie('login');

    if (window.location.origin.indexOf('file') !== -1) {
      document.body.classList.add("access-guaranted");
    } else {
      if (hasLogin.length == 0) {
        var sign = prompt("Access password:");
        if (loginSuccess(sign)) {
          document.body.classList.add("access-guaranted");
          setCookie('login', 'true', 1);
        } else {
          document.body.remove();
          setCookie('login', '', 1);
        }
      } else {
        document.body.classList.add("access-guaranted");
      }
    }

    function loginSuccess(b) {
      // var _0xe2d3=["\x45\x6E\x73\x61\x69\x6D\x61\x64\x61\x49\x67\x75\x61\x6C\x61\x64\x61"];var a=_0xe2d3[0]
      // return b && b === a;
      return true;
    }

    $(window).on('load resize', function () {
      //Add/remove class based on browser size when load/resize
      var w = $(window).width();

      if (w >= 1200) {
        // if larger 
        $('#docs-sidebar').addClass('sidebar-visible').removeClass('sidebar-hidden');
      } else {
        // if smaller
        $('#docs-sidebar').addClass('sidebar-hidden').removeClass('sidebar-visible');
      }
    });

    $(document).ready(function () {
      /* ====== Toggle Sidebar ======= */
      $('#docs-sidebar-toggler').on('click', function () {
        if ($('#docs-sidebar').hasClass('sidebar-visible')) {
          $("#docs-sidebar").removeClass('sidebar-visible').addClass('sidebar-hidden');
        } else {
          $("#docs-sidebar").removeClass('sidebar-hidden').addClass('sidebar-visible');
        }
      });

      /* ===== Smooth scrolling ====== */
      $(document).on('click', 'a[href^="#"]:not(.expand)', function (e) {
        //store hash
        var target = this.hash;
        
        if (!$(this).is('.anchorjs-link')) {
          // e.preventDefault();
        }

        $('body').scrollTo(target, 250, { offset: -69, 'axis': 'y' });

        // Collapse sidebar after clicking
        if ($('#docs-sidebar').hasClass('sidebar-visible') && $(window).width() < 1200) {
          $('#docs-sidebar').removeClass('sidebar-visible').addClass('slidebar-hidden');
        }
      });

      /* wmooth scrolling on page load if URL has a hash */
      if (window.location.hash) {
        var urlhash = window.location.hash;
        $('body').scrollTo(urlhash, 0, { offset: -69, 'axis': 'y' });
      }

      $('code.split').not('.split2dots').html(function(){
        return '<span>' + $(this).html().split('___').join('</span>___<span>') + '</span>';
      });
      $('code.split2dots').html(function(){
        var split = $(this).html().split(',');
        for (let i = 0; i < split.length; i++) {
          var split2 = '<span class="sub">' + split[i].split(':').join('</span>:<span class="sub">') + '</span>';
          split[i] = '<span class="el">' + split2 + '</span>';
        }
        return split.join(',');
      });

      $('h1.docs-heading, h2.section-heading, h3.section-heading').append(function () {
        var id = $(this).closest('.docs-section, .docs-article').attr('id');
        return '<a class="anchorjs-link" aria-label="Anchor" href="#' + id + '" style="padding-left: 0.375em;">#</a>';
      });
      
      var search_list = [];
      $('h1.docs-heading, h2.section-heading, h3.section-heading').not('.hide-search').each(function (index, el) {
        var id = $(this).closest('.docs-section, .docs-article').attr('id');
        var docsTime = '';

        if ($(this).find('.docs-time').length) {
          docsTime = $(this).find('.docs-time').text();
        }

        search_list.push({
          "text": $(this).text().replace('#', '').replace('opcional', ''),
          "id": id,
          "docsTime": docsTime,
        });
      });
      const options = {
        includeScore: false,
        keys: ['text'],
        minMatchCharLength: 2,
        threshold: 0.5,
      };
      const fuse = new Fuse(search_list, options);
      
      $('[name="search"]').on('input', function (event) {
        const result = fuse.search($(this).val());
        var list = '';
        for (let i = 0; i < result.length; i++) {
          const element = result[i];
          list += '<a href="#' + element.item.id + '">' + element.item.text.replace(element.item.docsTime, `<span>${element.item.docsTime}</span>`) + '</a>';
        }
        $(this).next('#results').html(list);
      });

      var Lversion = $('#changelogModal .modal-body h6').first().find('span').text().replace('Versión', '').replace('Version', '');;
      $('.site-logo .bg-primary').text('v' + Lversion);

      $('#changelogModal .modal-body ul a').click(function (event) {
        $('#changelogModal').modal('hide');
      });

      $('.modal').on('shown.bs.modal', function() {
        $(this).find('[autofocus]').focus();
      });

      setTimeout(() => {
        var el = $('.docs-nav .nav-link.active').first();
        if (el.length) {
          var elOffset = el.position().top;
          var elHeight = el.height();
          var windowHeight = $(window).height();
          var offset = 0;
          
          if (elHeight < windowHeight) {
            offset = elOffset - ((windowHeight / 2) - (elHeight / 2));
          }
          else {
            offset = elOffset;
          }
          $('#docs-sidebar').animate({ scrollTop: offset }, 0);
        }
      }, 250);
    });

    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('input', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  </script>

</body>

</html>
"""

# Usage example
folder_name = "example_folder"
web_link = WebLink(folder_name)
web_link.create_folder()
web_link.create_file_with_data(file_content)


# Adding header content
header_content = """
<header class="docs-header">
  <h1 class="docs-heading">Introduction <span class="docs-time">Secondary text</span></h1>
  <section class="docs-intro">
    <p>Section intro goes here. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque finibus
      condimentum nisl id vulputate. Praesent aliquet varius eros interdum suscipit. Donec eu purus sed nibh
      convallis bibendum quis vitae turpis. Duis vestibulum diam lorem, vitae dapibus nibh facilisis a. Fusce
      in malesuada odio.</p>
  </section>
  <h5>Github Code Example:</h5>
  <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Illo, possimus quae error nulla et, distinctio facilis iusto consectetur ullam provident unde neque cumque obcaecati omnis ipsa corrupti magnam dolor minima.</p>
  <h5>Highlight.js Example:</h5>
  <p>Lorem ipsum dolor sit amet <a href="#">consectetur</a> adipisicing elit. Nihil laudantium ex quis. Velit ad quibusdam alias dolorum exercitationem molestiae, commodi repellat culpa soluta vitae? Incidunt ratione esse quisquam nam earum.</p>
</header>
"""
web_link.add_header(header_content)

article_content = """
<article class="docs-article" id="section-python">
  <header class="docs-header">
    <h1 class="docs-heading">Python <span class="docs-time">Secondary text</span></h1>
  </header>
  <section class="docs-section" id="item-python-1">
    <h2 class="section-heading">Section Item Python 1</h2>
    <p>This is a new section added below the header.</p>
  </section>
</article>
"""

web_link.insert_article_below_comment("<!-- add article below -->", article_content)



