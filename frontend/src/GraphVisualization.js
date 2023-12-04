import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

// using d3
const GraphVisualization = ({ graphData }) => {
    const svgRef = useRef(null);
    const tooltipRef = useRef(null);

// fixed height and width
    const width = 900;
    const height = 600; 

    useEffect(() => {
        // setting attributes
        const svg = d3.select(svgRef.current)
            .attr('width', width)
            .attr('height', height)
            .style('border-radius', '20px')
            .style('border', '1px solid black');

        // clear on update
        svg.selectAll('*').remove();

        // initial display if no graph
        if (!graphData.nodes.length || !graphData.edges.length) {
            svg.append('text')
                .attr('x', width / 2)
                .attr('y', height / 2)
                .attr('text-anchor', 'middle')
                .text('Use scroll wheel to zoom in and out, hover over each vertex to display information!');
            return;
        }

       
        const g = svg.append('g');

        // zoom feature
        svg.call(d3.zoom().on('zoom', (event) => {
            g.attr('transform', event.transform);
        }));

        // tooltip div set up
        const tooltip = d3.select(tooltipRef.current)
            .style('opacity', 0)
            .style('position', 'absolute')
            .style('background-color', 'lightgrey')
            .style('padding', '5px')
            .style('border-radius', '5px')
            .style('pointer-events', 'none');

       
        const simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(120))
            .force('charge', d3.forceManyBody().strength(-400))
            .force('center', d3.forceCenter(width / 2, height / 2));

        // edges
        const link = g.selectAll('.link')
            .data(graphData.edges)
            .enter().append('line')
            .classed('link', true)
            .style('stroke', '#aaa')
            .style('stroke-width', 2);

        // draw nodes
        const node = g.selectAll('.node')
            .data(graphData.nodes)
            .enter().append('circle')
            .classed('node', true)
            .attr('r', 0) // Initialize with radius 0 for animation
            .style('fill', d => d.isCentral ? '#FFD700' : 'pink')
            .style('stroke', d => d.isCentral ? 'black' : 'black')
            .call(d3.drag()
                .on('start', dragStart)
                .on('drag', dragOn)
                .on('end', dragEnd));

       // cool transition
        node.transition()
            .duration(1350)
            .attr('r', d => d.isCentral ? 20 : 15);

        // mouseover for interaction
        node.on('mouseover', (event, d) => {
            const songList = d.songs.map(song => `<li>${song}</li>`).join('');
            const tooltipContent = `
                <strong>Artist:</strong> ${d.name}
                ${d.songs && d.songs.length ? `<br/><strong>Songs:</strong><ul>${songList}</ul>` : ''}
            `;
            tooltip.html(tooltipContent)
                .style('left', `${event.pageX + 10}px`)
                .style('top', `${event.pageY - 15}px`)
                .transition()
                .duration(300)
                .style('opacity', 0.9);
        })
        .on('mouseout', () => {
            tooltip.transition()
                .duration(500)
                .style('opacity', 0);
        });

       
        simulation.on('tick', () => {
            link.attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            node.attr('cx', d => d.x)
                .attr('cy', d => d.y);
        });

       	
        function dragStart(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragOn(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragEnd(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    }, [graphData]);

    return (
        <>
            <svg ref={svgRef}></svg>
            <div ref={tooltipRef}></div>
        </>
    );
};

export default GraphVisualization;
