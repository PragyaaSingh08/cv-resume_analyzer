// import React from 'react';
// import { useLocation } from 'react-router-dom';

// const Result = () => {
//   const location = useLocation();
//   const { resumeName, queryFileName, averageScore, results } = location.state || {};

//   return (
//     <div style={{ padding: '40px' }}>
//       <h2>Evaluation Result</h2>

//       <div style={{ marginBottom: '20px' }}>
//         <strong>Resume:</strong> {resumeName} <br />
//         <strong>Query File:</strong> {queryFileName} <br />
//         <strong>Average Score:</strong> {averageScore || 'N/A'}
//       </div>

//       <hr />

//       {results && results.length > 0 ? (
//         <div>
 
//          <h3>Detailed Questions</h3>
//           {results.map((item, idx) => (
//             <div key={idx} style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '8px' }}>
//               <strong>Q{idx + 1}:</strong> {item.query} <br />

//               {item.response ? (
//                 <>
//                   <strong>Score:</strong> {item.response.score || 'N/A'} <br />
//                   <strong>Status:</strong> {item.response.status || 'N/A'} <br />
//                   <strong>Matched Keywords:</strong> {item.response.matched_keywords?.join(', ') || 'None'} <br />
//                   <strong>Missing Keywords:</strong> {item.response.missing_keywords?.join(', ') || 'None'} <br />
//                   <strong>Explanation:</strong> {item.response.explanation || 'N/A'} <br />
//                 </>
//               ) : (
//                 <>
//                   <strong>Error:</strong> {item.error || 'Unknown error'} <br />
//                   <strong>Raw Output:</strong> {item.raw_output || 'N/A'}
//                 </>
//               )}
//             </div>
//           ))}
//         </div>
//       ) : (
//         <p>No detailed results to show.</p>
//       )}
//     </div>
//   );
// };
// export default Result;
import React from 'react';
import { useLocation } from 'react-router-dom';

const Result = () => {
  const location = useLocation();
  const { resumeName, queryFileName, averageScore, results } = location.state || {};

  // Utility function to safely convert to array and join
  const formatList = (value) => {
    if (Array.isArray(value)) return value.join(', ');
    if (typeof value === 'string') {
      try {
        const parsed = JSON.parse(value);
        return Array.isArray(parsed) ? parsed.join(', ') : value;
      } catch {
        return value;
      }
    }
    return 'None';
  };

  return (
    <div style={{ padding: '40px' }}>
      <h2>Evaluation Result</h2>

      <div style={{ marginBottom: '20px' }}>
        <strong>Resume:</strong> {resumeName} <br />
        <strong>Query File:</strong> {queryFileName} <br />
        <strong>Average Score:</strong> {averageScore !== undefined ? averageScore.toFixed(2) : 'N/A'}
      </div>

      <hr />

      {results && results.length > 0 ? (
        <div>
          <h3>Detailed Questions</h3>
          {results.map((item, idx) => (
            <div key={idx} style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '8px' }}>
              <strong>Q{idx + 1}:</strong> {item.query} <br />

              {item.response ? (
                <>
                  <strong>Score:</strong> {item.response.score || 'N/A'} <br />
                  <strong>Status:</strong> {item.response.status || 'N/A'} <br />
                  <strong>Matched Keywords:</strong> {formatList(item.response.matched_keywords)} <br />
                  <strong>Missing Keywords:</strong> {formatList(item.response.missing_keywords)} <br />
                  <strong>Explanation:</strong> {item.response.explanation || 'N/A'} <br />
                </>
              ) : (
                <>
                  <strong>Error:</strong> {item.error || 'Unknown error'} <br />
                  <strong>Raw Output:</strong> {item.raw_output || 'N/A'}
                </>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p>No detailed results to show.</p>
      )}
    </div>
  );
};

export default Result;
