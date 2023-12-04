export function convertToGraphData(collaborations, mainArtistId) {
  console.log("Received data:", collaborations);

  // empty array for nodes
  var nodes = [];
  for (var i = 0; i < collaborations.length; i++) {
    var artist = collaborations[i];
    nodes.push({
      id: artist.id,
      name: artist.name,
      songs: artist.songs ? artist.songs : []
    });
  }

  // create edges
  var edges = [];
  for (var j = 0; j < collaborations.length; j++) {
    var collaborator = collaborations[j];
    edges.push({
      source: mainArtistId,
      target: collaborator.id
    });
  }

  // find artist and make it the central element
  var mainArtistIndex = -1;
  for (var k = 0; k < nodes.length; k++) {
    if (nodes[k].id === mainArtistId) {
      mainArtistIndex = k;
      break;
    }
  }
  if (mainArtistIndex !== -1) {
    nodes[mainArtistIndex].isCentral = true;
  }

  return {
    nodes: nodes,
    edges: edges
  };
};
