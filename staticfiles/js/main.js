// main.js

document.addEventListener("DOMContentLoaded", function() {


  

 
    // ---- Copy buttons for code blocks ----
    document.querySelectorAll("pre code").forEach(function(codeBlock) {
        const button = document.createElement("button");
        button.innerText = "Copy";
        button.className = "copy-btn";
        const pre = codeBlock.parentNode;
        pre.parentNode.insertBefore(button, pre);

        button.addEventListener("click", function() {
            navigator.clipboard.writeText(codeBlock.innerText).then(function() {
                button.innerText = "Copied!";
                setTimeout(() => button.innerText = "Copy", 1500);
            });
        });
    });

    // ---- Table of Contents ----
    // const tocContainer = document.getElementById("toc");
    // if (tocContainer) {
    //     const headings = document.querySelectorAll(".post-body h2, .post-body h3");
    //     if (headings.length > 0) {
    //         let tocList = document.createElement("ul");
    //         tocList.style.listStyleType = "none";
    //         tocList.style.paddingLeft = "0";

    //         headings.forEach(function(heading, index) {
    //             const id = "section-" + index;
    //             heading.id = id;

    //             let li = document.createElement("li");
    //             li.style.marginBottom = "5px";
    //             li.style.position = "relative";
    //             li.style.paddingLeft = heading.tagName === "H3" ? "35px" : "25px";

    //             const bullet = document.createElement("span");
    //             bullet.innerText = heading.tagName === "H2" ? "●" : "○";
    //             bullet.style.position = "absolute";
    //             bullet.style.left = heading.tagName === "H3" ? "10px" : "0";
    //             bullet.style.color = "#CC6B49";
    //             bullet.style.fontSize = "0.8em";
    //             bullet.style.lineHeight = "1";

    //             const a = document.createElement("a");
    //             a.href = "#" + id;
    //             a.innerText = heading.innerText;
    //             a.style.textDecoration = "none";
    //             a.style.color = "#6F5643";
    //             a.style.transition = "all 0.2s";

    //             a.addEventListener("mouseenter", () => a.style.textDecoration = "underline");
    //             a.addEventListener("mouseleave", () => a.style.textDecoration = "none");

    //             li.appendChild(bullet);
    //             li.appendChild(a);
    //             tocList.appendChild(li);
    //         });

    //         const tocHeading = document.createElement("h5");
    //         tocHeading.innerText = "Table of Contents";
    //         tocHeading.style.fontWeight = "700";
    //         tocHeading.style.marginBottom = "10px";

    //         tocContainer.innerHTML = "";
    //         tocContainer.appendChild(tocHeading);
    //         tocContainer.appendChild(tocList);
    //     }
    // }
// const tocContainer = document.getElementById("toc");
// if (tocContainer) {
//     const headings = document.querySelectorAll(".post-body h2, .post-body h3");
//     if (headings.length > 0) {
//         const tocList = document.createElement("ul");
//         tocList.style.listStyleType = "none";
//         tocList.style.paddingLeft = "0";

//         headings.forEach((heading, index) => {
//             const id = "section-" + index;
//             heading.id = id;

//             const li = document.createElement("li");
//             li.style.display = "flex";            // use flex for alignment
//             li.style.alignItems = "top";
//             li.style.lineHeight = "1.4";
//             li.style.marginBottom = "4px";
//             li.style.paddingLeft = heading.tagName === "H3" ? "25px" : "0";

//             const bullet = document.createElement("span");
//             bullet.innerText = heading.tagName === "H2" ? "●" : "○";
//             bullet.style.color = "#CC6B49";
//             bullet.style.fontSize = "0.8em";
//             bullet.style.marginRight = "8px";     // space between bullet and text
//             bullet.style.lineHeight = "1.4";

//             const a = document.createElement("a");
//             a.href = "#" + id;
//             a.innerText = heading.innerText;
//             a.style.textDecoration = "none";
//             a.style.color = "#6F5643";
//             a.style.transition = "all 0.2s";

//             a.addEventListener("mouseenter", () => a.style.textDecoration = "underline");
//             a.addEventListener("mouseleave", () => a.style.textDecoration = "none");

//             li.appendChild(bullet);
//             li.appendChild(a);
//             tocList.appendChild(li);
//         });

//         // const tocHeading = document.createElement("h5");
//         // tocHeading.innerText = "Table of Contents";
//         // tocHeading.style.fontWeight = "700";
//         // tocHeading.style.marginBottom = "10px";

//         tocContainer.innerHTML = "";
//         // tocContainer.appendChild(tocHeading);
//         tocContainer.appendChild(tocList);
//     }
// }
// Only handle clicks on TOC links for smooth scrolling
const tocContainer = document.getElementById("toc");
if (tocContainer) {
    const links = tocContainer.querySelectorAll("a[href^='#']");
    links.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const target = document.getElementById(this.getAttribute("href").substring(1));
            if (target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        });

        // Optional: hover effect already handled in CSS
        link.addEventListener("mouseenter", () => link.style.textDecoration = "underline");
        link.addEventListener("mouseleave", () => link.style.textDecoration = "none");
    });
}
  const sidebar = document.getElementById("sidebarMenu");
    const toggleBtn = document.getElementById("toggleBtn");

    toggleBtn.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });

document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'load-more-comments') {
        const btn = e.target;
        const nextPage = btn.dataset.nextPage;
        fetch(window.location.pathname + '?page=' + nextPage, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(res => res.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newCommentsList = doc.getElementById('comments-list').innerHTML;
            document.getElementById('comments-list').insertAdjacentHTML('beforeend', newCommentsList);

            // Update the button
            const newBtn = doc.getElementById('load-more-comments');
            if (newBtn) {
                btn.dataset.nextPage = newBtn.dataset.nextPage;
            } else {
                btn.remove();
            }
        });
    }
});

// document.addEventListener('DOMContentLoaded', function() {
//     const img = document.querySelector('.hero-img');
//     img.classList.add('loaded'); // triggers CSS transition
// });

});
