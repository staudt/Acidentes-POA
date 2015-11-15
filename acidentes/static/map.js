var map, heatmap, marcador, interval_id, via_ranking, infowindow;

$(function() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -30.081143, lng: -51.185737},
        zoom: 12
    });
    google.maps.event.addListener(map, 'zoom_changed', function() {
        if (map.getZoom() > 15) map.setZoom(15);
    });
    interval_id = loading();
    google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
        interval_id = loading();
        carregaTabela();
    });
    $('.filtro').change(function () {
        interval_id = loading();
        carregaTabela();
    });
});

function montaUrl(endpoint) {
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
    if (endpoint == "top") {
        return '/query/top/50?' + query.join('&');
    }
    else {
        return '/';
    }
}

function loadsLineChart(via, count) {
    $('#linechart').remove();
    $.ajax({
      url: '/query/via/' + via + '?ranking=' + $('select#ranking').val(),
      type: 'GET',
      success: function(data) {
        results = $.parseJSON(data);
        $('#grafico_via').html('').sparkline(results, {
            type: 'line',
            width: '100%',
            height: '30',
            fillColor: undefined,
            chartRangeMin: 0,
            normalRangeMin: 0,
            normalRangeMax: count,
            drawNormalOnTop: true
        });
      },
      error : function(data) {
        $('#grafico_via').html('Não foi possivel extrair dados da via');
      }
    });
}

function marcarNoMapa(via) {
    if (typeof marcador != "undefined") {
        marcador.setMap(null);
    }
    var geo = via_ranking[via]["latlang"].split(";"),
        latitude = parseFloat(geo[0]),
        longitude = parseFloat(geo[1]);
    marcador = new google.maps.Marker({
        position: {lat: latitude, lng: longitude},
        map: map,
        title: via
    });
    var contentString = '<div>' +
        '<center><b>'+ via +'</b></center><br/>' +
        'Contagem: <b>' + via_ranking[via]["ranking"] + '</b> (' + via_ranking[via]["perc"] + '%)' +
        '<br/><br/>Histórico Anual:<br/><div id="grafico_via"><center><img src="static/loading.gif"/></center></div>'
      '</div>'
    infowindow = new google.maps.InfoWindow({ content: contentString });
    loadsLineChart(via, via_ranking[via]["ranking"]);
    infowindow.open(map, marcador);
    map.panTo({lat: latitude, lng: longitude});
    marcador.addListener('click', function() {
        infowindow.open(map, marcador);
    });
}

function loading(){
    if (interval_id) return interval_id;
    $('#tabela .ranking').remove();
    $('#tabela tr:last').after('<tr class="ranking loading"><td colspan="4"><center><img src="static/loading.gif"/></center></td></tr>');
    return interval_id;
}

function carregaTabela() {
    interval_id = loading();
    if (typeof heatmap != "undefined") {
        heatmap.setMap(null);
    }
    if (typeof marcador != "undefined") {
        marcador.setMap(null);
    }    
    $('#linechart').remove();
    $.ajax({
      url: montaUrl("top", ""),
      type: 'GET',
      success: function(data) {
        if (interval_id){
            clearInterval(interval_id);
            interval_id = null;
        }
        $('#tabela .ranking').remove();
        results = $.parseJSON(data);
        var total = 0;
        via_ranking = {}
        $.each(results['top'], function(i, item) {
            total += item.ranking;
            via_ranking[item.via] = {}
            via_ranking[item.via]['ranking'] = parseInt(item.ranking);
            via_ranking[item.via]['latlang'] = item.latlng;
        });
        $.each(via_ranking, function (via, dict) {
            via_ranking[via]['perc'] = ((dict['ranking']/total)*100).toFixed(2);
            $('#tabela tr:last').after(
                '<tr class="ranking">'+
                    '<td><a href="#" onclick="marcarNoMapa(\''+ via +'\')">' + via + '</a></td>'+
                    '<td class="contagem">' + dict['ranking'] + '</td>'+
                    '<td class="percent">' + dict['perc'] + '</td>'+
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
                value = via_ranking[via]['ranking'];
            heatmap_locations.push({
                location : new google.maps.LatLng(lat, lg),
                weight: value /*Change to 1 if needed*/
            });
        });
        if (heatmap_locations.length > 0){
            heatmap = new google.maps.visualization.HeatmapLayer({
                data: heatmap_locations,
                radius: 15,
                map: map
            });
        }
        else {
            $('#tabela tr:last').after('<tr class="ranking"><td colspan="4">Sem dados. Tente outro filtro.</td></tr>');
        }
      },
      error : function(data) {
        if (interval_id){
            clearInterval(interval_id);
            interval_id = null;
        }
        $('#tabela .ranking').remove();
        $('#tabela tr:last').after('<tr class="ranking"><td colspan="4">Erro ao tentar extrair dados. Tem certeza que o servidor esta rodando?</td></tr>');
      }
    });
}

