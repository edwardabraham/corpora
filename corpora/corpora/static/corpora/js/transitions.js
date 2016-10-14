function nextPageTransition(currPage, nextPage) {
	currPage.addClass("pt-page-moveToLeft pt-page-fadeOut");
	nextPage.addClass("pt-page-current pt-page-moveFromRight");

	currPage.one("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd",   
		function(e) {
			nextPage.removeClass("pt-page-moveFromRight");
			currPage.removeClass("pt-page-current pt-page-moveToLeft pt-page-fadeOut");
	});
}

function prevPageTransition(currPage, prevPage) {
	currPage.addClass("pt-page-moveToRight pt-page-fadeOut");
	prevPage.addClass("pt-page-current pt-page-moveFromLeft");
	
	currPage.one("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd",
		function(e) {
			prevPage.removeClass("pt-page-moveFromLeft");
			currPage.removeClass("pt-page-current pt-page-moveToRight pt-page-fadeOut");
	});
}