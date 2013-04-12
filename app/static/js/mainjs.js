  // Tutorial JS 
  $('#start_me').live('click', function(){
    $('#top_instruction').fadeOut('medium', function(){
      $('#error_message').hide();
      $('#lower_instruction').html('Name a class you\'re taking').attr('class', 'lead');
      $('#start_me').hide();
      $('#friend_div').fadeIn('slow');
    });
  });

