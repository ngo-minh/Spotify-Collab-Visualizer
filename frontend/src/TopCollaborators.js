import React from 'react';

const TopCollaborators = ({ collaborators }) => {
  return (
    <div className="top-collaborators">
      <h3>Top 10 Collaborators</h3>
      <ul>
        {collaborators.map((collaborator, index) => (
          <li key={index}>
            {collaborator.name} - {collaborator.song_count} songs
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TopCollaborators;
