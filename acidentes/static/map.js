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

function parseJSONToHeatmap(data) {
    var heatmap_locations = [];
    $.each($.parseJSON(data), function(i, item) {
        var via = item.via,
            ranking = item.ranking,
            points = item.points,
            bound = new google.maps.LatLngBounds();        
        if (points){
            $.each(points, function (j, jitem) { 
                heatmap_locations.push({location: new google.maps.LatLng(parseFloat(jitem.latitude), parseFloat(jitem.longitude)), weight: parseFloat(ranking)});
                bound.extend( new google.maps.LatLng(parseFloat(jitem.latitude), parseFloat(jitem.longitude)));
            });            
        }
        else{// damn 'total' falls here, only a single point to parse
            heatmap_locations.push({location: new google.maps.LatLng(parseFloat(item.latitude), parseFloat(item.longitude)), weight: 10*parseFloat(ranking)});
            bound.extend( new google.maps.LatLng(parseFloat(item.latitude), parseFloat(item.longitude)));
        }
        $('#tabela tr:last').after('<tr class="ranking"><td>' + ranking + '</td>'+
        '<td><a href="#" onclick="marcarNoMapa(\''+ via +'\', '+ bound.getCenter().lat() +', '+ bound.getCenter().lng() +')">' + via + '</a></td>'+'</tr>');
    })
    return heatmap_locations;
}

function carregaTabela() {
    $('#tabela .ranking').remove();
    if (typeof heatmap != "undefined") {
        heatmap.setMap(null);
    }
    $.ajax({
      url: '/query/top/'+ $('#busca option:selected').val() +'/10',
      type: 'GET',
      success: function(data) {
        var heatmap_locations = parseJSONToHeatmap(data);
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmap_locations,
            radius: 40,
            map: map
        });
      },
      error : function(data) {	         
        $('#tabela tr:last').after('<tr class="ranking"><td colspan="4">Erro ao tentar extrair dados. Tem certeza que o servidor esta rodando?</td></tr>');
      }
    });
}

