document.addEventListener("DOMContentLoaded", function() {
  const paragraphs = document.querySelectorAll(".card-body .text-feed p");
  const charLimit = 200; // The character limit before the "Read More" link appears

  paragraphs.forEach(paragraph => {
      const fullText = paragraph.innerHTML.trim();


      

      if (fullText.length > charLimit)
      {
        const visibleText = fullText.slice(0, charLimit);
        const hiddenText = fullText.slice(charLimit);

        console.log(visibleText + visibleText.length);

        paragraph.innerHTML =  `${visibleText}<span class="more-text">${hiddenText}</span>
              <span class="read-more" id="toggle-button">Read More</span>`;

        // const toggleButton = paragraph.querySelector(".read-more");
        // const moreText = paragraph.querySelector(".more-text");

        // toggleButton.onclick = () =>{
        //     if (moreText.style.display === "none" || moreText.style.display === "") {
        //       moreText.style.display = "inline";
        //       toggleButton.textContent = "Read Less";
        //     }
        //     else {
        //       moreText.style.display = "none";
        //       toggleButton.textContent = "Read More";
        //     }
        // }
  
      }
      
      // if (fullText.textContent.length > charLimit) {
      //     const visibleText = fullText.textContent.slice(0, charLimit);
      //     const hiddenText = fullText.textContent.slice(charLimit);

      //     paragraph.innerHTML = `
      //         ${visibleText}<span class="more-text">${hiddenText}</span>
      //         <span class="read-more" id="toggle-button">Read More</span>`;

      //     const toggleButton = paragraph.querySelector(".read-more");
      //     const moreText = paragraph.querySelector(".more-text");

      //     toggleButton.addEventListener("click", function() {

      //     });
      // }
  });
});
