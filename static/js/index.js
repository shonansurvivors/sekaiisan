$(function(){

  $('.countryList__item').mouseover(function(){
    $(this).css('opacity', '0.6');
  });

  $('.countryList__item').mouseleave(function(){
    $(this).css('opacity', '');
  });

  $('.heritageList__item').mouseover(function(){
    $(this).css('opacity', '0.6');
  });

  $('.heritageList__item').mouseleave(function(){
    $(this).css('opacity', '');
  });


  var howToDetailPosition = [];

  howToDetailPosition[0] = $('.howto__detail--1').offset().top;
  howToDetailPosition[1] = $('.howto__detail--2').offset().top;
  howToDetailPosition[2] = $('.howto__detail--3').offset().top;

  var countryListPosition = $('.countryList').offset().top;
  var heritageListPosition = $('.heritageList').offset().top;

  var stopFlag = false

  $(window).scroll(function(){
    if(stopFlag){
      return;
    }else{

      var lastScrollPosition = $(window).scrollTop() + window.innerHeight;

      if(lastScrollPosition > howToDetailPosition[0]){
        $('.howto__detail--1').addClass('howto__detail--isAnimation');
      };
      if(lastScrollPosition > howToDetailPosition[1]){
        $('.howto__detail--2').addClass('howto__detail--isAnimation');
      };
      if(lastScrollPosition > howToDetailPosition[2]){
        $('.howto__detail--3').addClass('howto__detail--isAnimation');
      };

      if(lastScrollPosition > countryListPosition){
        $('.countryList').addClass('countryList--isAnimation');
      };

      if(lastScrollPosition > heritageListPosition){
        $('.heritageList').addClass('heritageList--isAnimation');
        stopFlag = true;
      };
    };
  });
});
