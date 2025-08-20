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

	// Close the image on 'esc'
	document.addEventListener('keydown', (event) => {	
		if (MainGallery.classList.contains('active') && event.key === 'Escape') {
			MainGallery.classList.remove('active');
		}
	});

	//Using list of galleries, add function to open to each
	galleries.forEach(gallery => {
	
		//For each image within gallery
		const images = gallery.querySelectorAll('img');
		images.forEach((img, index) => {
			
			//Make each image appear clickable
			img.style.cursor = 'pointer';
			
			//On click:
			//	add the images from the current div to the MainGallery, set the index, then show the Main Gallery
			img.addEventListener('click', () => {
				currentGalleryImages = Array.from(images);
				showImage(index);
				MainGallery.classList.add('active');				
			});
		});
	});
});
