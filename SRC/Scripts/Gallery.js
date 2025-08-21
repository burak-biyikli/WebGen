//Wait for page to load
document.addEventListener('DOMContentLoaded', () => {

	//Find everything with the given class
	const galleries = document.querySelectorAll(".image-gallery")

	//Nothing to do, no galleries on page
  	if (galleries.length === 0){
  		return;
  	}
  	
  	//Create the model where images show up when clicked
	const MainGallery = document.createElement('div');
	MainGallery.className = 'MainGallery'
	MainGallery.innerHTML = `
	<span class="gallery-close">&times;</span>
	<span class="gallery-nav prev">&lt;</span>
	<span class="gallery-nav next">&gt;</span>
	<img src="" alt="Fullscreen image">`;
	document.body.appendChild(MainGallery);

	//Create vars for state
	const MainGalleryImg = MainGallery.querySelector('img');
	let currentGalleryImages = [];
	let currentIndex = 0;

	//Function that updates visible state
	function showImage(index) {
		currentIndex = (index + currentGalleryImages.length) % currentGalleryImages.length;
		MainGalleryImg.src = currentGalleryImages[currentIndex].src;
		MainGalleryImg.alt = currentGalleryImages[currentIndex].alt;
		MainGallery.querySelector('.next').style.display = currentGalleryImages.length > 1 ? 'block' : 'none';
		MainGallery.querySelector('.prev').style.display = currentGalleryImages.length > 1 ? 'block' : 'none';
	}

	// Add event listeners
	MainGallery.querySelector('.gallery-close').addEventListener('click', () => { MainGallery.classList.remove('active'); });
	MainGallery.querySelector('.prev').addEventListener('click', () => { showImage(currentIndex-1); });
	MainGallery.querySelector('.next').addEventListener('click', () => { showImage(currentIndex+1); });

	// Close the image on 'esc', left and right from arrow keys
	document.addEventListener('keydown', (event) => {	
		if (!MainGallery.classList.contains('active')){
			return;
		} else if (event.key === 'Escape') {
			MainGallery.classList.remove('active');
		} else if (event.key === 'ArrowLeft') {
			showImage(currentIndex-1);
		} else if (event.key === 'ArrowRight') {
			showImage(currentIndex+1)
		}
	});
	

	//Using list of galleries, add function to open to each
	galleries.forEach( (gallery, gidx) => {
	
		//For each image within gallery
		const images = gallery.querySelectorAll('img');
		const sep_width = (images.length + 1) * 2; //Amount of gap in percent 
		const def_width = Math.min( 60, (100 - sep_width)/images.length) + "%"
		//console.log("Found default width of: "def_width + " for " + gidx);
		
		images.forEach((img, iidx) => {
			
			//Make each image appear clickable
			img.style.cursor = 'pointer';
			
			img.style.width = img.style.width == "" ? def_width : img.style.width; 
			
			//On click:
			//	add the images from the current div to the MainGallery, set the index, then show the Main Gallery
			img.addEventListener('click', () => {
				currentGalleryImages = Array.from(images);
				showImage(iidx);
				MainGallery.classList.add('active');				
			});
		});
	});
});
