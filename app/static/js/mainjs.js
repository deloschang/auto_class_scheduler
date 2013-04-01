  // Tutorial JS 
  $('#start_me').live('click', function(){
    try{
      mixpanel.track("Clicked LetsStart button tutorial");
    } catch(e) {
      console.log('start');
    }
    $('#top_instruction').fadeOut('medium', function(){
      $('#lower_instruction').html('Name a class you\'re taking').attr('class', 'lead');
      $('#start_me').hide();
      $('#friend_div').fadeIn('slow');
    });
  });

