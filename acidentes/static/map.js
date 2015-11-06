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
    $('#tabela .ranking').remove();
    if (typeof heatmap != "undefined") {
        heatmap.setMap(null);
    }
    $.ajax({
      url: '/query/top/50',
      type: 'GET',
      success: function(data) {
        results = $.parseJSON(data);
        $.each(results['top'], function(i, item) {
            $('#tabela tr:last').after('<tr class="ranking"><td>' + item.ranking + '</td>'+
                '<td><a href="#" onclick="marcarNoMapa(\''+ item.via +'\', '+ item.latlng.replace(';', ', ') +')">' + item.via + '</a></td>'+'</tr>');
        });
        var heatmap_locations = [];
        $.each(results['coordenadas'], function(i, item) {
            heatmap_locations.push(
                new google.maps.LatLng(
                    parseFloat(item.split(';')[0]),
                    parseFloat(item.split(';')[1])
                )
            );
        });
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmap_locations,
            radius: 10,
            map: map
        });
      },
      error : function(data) {	         
        $('#tabela tr:last').after('<tr class="ranking"><td colspan="4">Erro ao tentar extrair dados. Tem certeza que o servidor esta rodando?</td></tr>');
      }
    });
}

