function loadSamples(){
    url="/names";    
    Plotly.d3.json(url, function(error, response) {
        if (error) return console.warn(error);
        for(i=0;i<response.length;i++){
            var opt = document.createElement("option");
            opt.setAttribute("value", response[i]);

            var optt = document.createTextNode(response[i]);
            opt.appendChild(optt);

            document.querySelector("#selDataset")
                .appendChild(opt);
        }
    });

}

function optionChanged(val){
    url="/samples/"+val;
    Plotly.d3.json(url, function(error, response) {
        if (error) return console.warn(error);
        console.log(response);
        var values=[];
        var labels=[];
        for(i=0;i<10;i++){
            values.push(response.sample_values[i]);
            labels.push(response.otu_ids[i]);
        }
        var data = [{
            values: values,
            labels: labels,
            type: 'pie'
          }];
          
          var layout = {
            height: 400,
            width: 500
          };
          Plotly.newPlot('myPie', data, layout);  
    })
}
loadSamples();