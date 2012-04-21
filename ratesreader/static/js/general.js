$(function() {
    $.getJSON('exchange-rates', function(data) {
        for (i = 0; i <= data.length-1; i++){
            var rate = data[i]
            //var url = 'http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?';
            var url = 'rate-history/'+rate
            $.getJSON(url, function(rates) {
                // Create the chart
                window['chart_'+rates.name] = new Highcharts.StockChart({
                    chart : {
                        renderTo : rates.name,
                        height: 200,
                        width: 400
                    },
                    rangeSelector : {
                        selected : 1,
                        inputEnabled: false
                    },
                    scrollbar : {
                        enabled : false
                    },
                    title : {
                        text: 'EUR to ' + rates.name.toUpperCase()
                    },
                    series : [{
                        name : 'EUR to ' + rates.name.toUpperCase(),
                        data : rates.data,
                        tooltip: {
                            valueDecimals: 2
                        }
                    }]
                });
            });
        }
    });
});