   import React, { useState } from 'react';
   import axios from 'axios';

   function App() {
     const [currentTime, setCurrentTime] = useState('');

     const fetchCurrentTime = async () => {
       try {
         const response = await axios.get('http://localhost:8000/current-time');
         setCurrentTime(response.data.current_time);
       } catch (error) {
         console.error("Error fetching the current time:", error);
       }
     };

     return (
       <div style={{ textAlign: 'center', marginTop: '50px' }}>
         <h1>Current Date and Time</h1>
         <button onClick={fetchCurrentTime}>Get Current Time</button>
         {currentTime && <p>The current time is: {currentTime}</p>}
       </div>
     );
   }

   export default App;
   