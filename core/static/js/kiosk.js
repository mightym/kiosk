var kkCom = {
  channel: null,
  initialize: function() {
    console.log('init');
    var transport = WebSocket; //SockJS
    var connection = new Omnibus(transport, omnibusEndpoint, omnibusOptions); // omnibusEndpoint, omnibusOptions defined/parsed in base.html
    kkCom.channel = connection.openChannel('slide_update');

    this.bindEvents();
  },
  bindEvents: function() {
    console.log('bind');

    kkCom.channel.on('published', function (event) {
      console.log('data'+event.data);
      location.reload();
      // $('.chat-messages ul').append('<li>'+event.data.payload.user+': ' +event.data.payload.body+'</li>');
    });

  }
}

kkCom.initialize();