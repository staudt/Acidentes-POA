
/* Este bloco só roda depois que a pagina esta carregada */
$(function() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -30.081143, lng: -51.185737},
        zoom: 12
    });
    google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
        carregaTabela();
    });
    $('.filtro').change(function () {
        carregaTabela();
    });
});

var map, heatmap, marcador;

function marcarNoMapa(via, latitude, longitude) {
    if (typeof marcador != "undefined") {
        marcador.setMap(null);
    }
    marcador = new google.maps.Marker({
        position: {lat: latitude, lng: longitude},
        map: map,
        title: via
    });
    map.panTo({lat: latitude, lng: longitude});
}

function carregaTabela() {
    function montaUrl() {
        var query = [
            'ano=' + $('select#ano').val(),
            'ranking=' + $('select#ranking').val(),
            'tipo_acid=' + $('select#tipo_acid').val(),
            'mes=' + $('select#mes').val(),
            'dia_sem=' + $('select#dia_sem').val(),
            'auto=' + ($('#auto').prop('checked') ? 1 : ''),
            'moto=' + ($('#moto').prop('checked') ? 1 : ''),
            'taxi=' + ($('#taxi').prop('checked') ? 1 : ''),
            'lotacao=' + ($('#lotacao').prop('checked') ? 1 : ''),
            'onibus=' + ($('#onibus').prop('checked') ? 1 : ''),
            'caminhao=' + ($('#caminhao').prop('checked') ? 1 : ''),
            'bicicleta=' + ($('#bicicleta').prop('checked') ? 1 : '')
        ];
        return '/query/top/50?' + query.join('&');
    }
    ;
    $('#tabela .ranking').remove();
    if (typeof heatmap != "undefined") {
        heatmap.setMap(null);
    }
    $.ajax({
      url: montaUrl(),
      type: 'GET',
      success: function(data) {
        results = $.parseJSON(data);
        var via_ranking = {},
            via_latlng = {},
            total = 0;
        $.each(results['top'], function(i, item) {
            total += item.ranking;
            via_ranking[item.via] = parseInt(item.ranking);
            via_latlng[item.via] = item.latlng.replace(';', ', ');
        });
        $.each(via_ranking, function (via, ranking) {
            $('#tabela tr:last').after(
                '<tr class="ranking">'+
                    '<td><a href="#" onclick="marcarNoMapa(\''+ via +'\', '+ via_latlng[via] +')">' + via + '</a></td>'+
                    '<td class="contagem">' + ranking + '</td>'+
                    '<td class="percent">' + ((ranking/total)*100).toFixed(2) + '</td>'+
                '</tr>'
            );
        });            
        var heatmap_locations = [];
        $.each(results['coordenadas'], function(i, item) {
            var ranking = $('select#ranking').val();
            var items = item.split(';'),
                lat = parseFloat(items[0]),
                lg = parseFloat(items[1]),
                via = items[2],
                value = via_ranking[via];
            heatmap_locations.push({
                location : new google.maps.LatLng(lat, lg),
                weight: value /*Change to 1 if needed*/
            });
        });
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmap_locations,
            /*radius: 10,*/
            map: map
        });
      },
      error : function(data) {	         
        $('#tabela tr:last').after('<tr class="ranking"><td colspan="4">Erro ao tentar extrair dados. Tem certeza que o servidor esta rodando?</td></tr>');
      }
    });
}

