jQuery(function($){

  var in_call = false;

  if ( $("#id").length ) id = $("#id").text(); 

  $(window).keydown(function(e){
    if ( e.keyCode > 47 && e.keyCode < 58 ) { get_call(String.fromCharCode(e.keyCode)); }
    else if ( e.keyCode == 13 ) submit();
    return true;
  });

  $("#menu p").click(function() {
    var id = $(this).text();
    $("#"+id).show().click(function() { $(this).hide(); });
  });

  $("#number p").click(function() { get_call($(this).text()); });

  $("#clear").click(function() { clear(); });

  $("#submit").click(function() { submit(); });

  $("#reload").click(function() { location.reload(); });

  $("h1").click(function() { refresh(); });

  $("#card").click(function() {
    var card = $("#card span").text();
    if ( card.match("[3-5]") ) {
      card = parseInt(card) != 5 ? parseInt(card) + 1 : 3;
      $("#card span").text(card);
      refresh();
    }
  });

  function refresh() {
    var card = $("#card span").text();
    if ( card.match("[3-5]") ) {
      $.getJSON("",{"card":card},function(json) {
        $("#id").text(json.id);
        $("#card span").text(json.card);
      });
      $("table tr:nth-child(n+2)").remove();
      clear();
      in_call = false;
    }
  }

  function get_call(num) {
    var len = parseInt($("#card span").text());
    if ( in_call ) return;
    val = $("h1").text();
    re = new RegExp(num);
    if ( val.match(re) ) {
      val = val.replace(re,"");
      $("#n"+num).attr("class","on");
    } else if ( val.length < len ) {
      val += num; 
      $("#n"+num).attr("class","off");
    } else if ( val.length > len ) {
      val = num; 
      $("#n"+num).attr("class","off");
    }
    check(val,len);
  }

  function check(val,len) {
    if ( val == "" ) { clear(); }
    else if ( val.length <= len ) {
      $("h1").text(val);
      $("#clear").css({"color":"#fff","border":"2px solid #fff"});
      if ( val.length == len ) {
        $("#submit").css({"color":"#fff","border":"2px solid #fff"});
        $("p.on").css({"color":"#999","border":"2px solid #999"});
      } else {
        $("p.on").attr("style","");
        $("#submit").attr("style","");
      }
    }
  }

  function submit() {
    if ( in_call ) return;
    var call = $("h1").text();
    var len = parseInt($("#card span").text());
    if ( call.length == len ) {
      $("#loading").show(); $("body").css("cursor","wait");
      in_call = true;
      $.getJSON("",{"id":id,"call":call,"card":len},function(json) {
        $("<tr>").append($("<td>").text(call)).append($("<td>").text(json.e)).append($("<td>").text(json.b)).appendTo($("table"));
        clear();
        $("#overlay, #loading").hide(); $("body").css("cursor","auto");
        if ( json.e == len ) {
          $("#win").show().click(function() { $(this).hide(); });
        } else {
          in_call = false;
        }
      });
    }
  }

  function clear() {
    $("h1").text("numerÖn");
    $("p.off").attr("class","on");
    $("p.on").attr("style","");
    $("button").attr("style","");
  }

});
