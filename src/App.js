import React, { useState, useEffect } from 'react';
import './App.css';
import PixelBlast from './Background';
import LeafComponent from './components/LeafComponent';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [streamError, setStreamError] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [sensorValue, setSensorValue] = useState('Loading...');
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [plantData, setPlantData] = useState({
    guava: { color: '-', status: '-', health_score: '-', issues: '-' },
    mexican: { color: '-', status: '-', health_score: '-', issues: '-' },
    lemon: { color: '-', status: '-', health_score: '-', issues: '-' }
  });
  const [plantAnalysis, setPlantAnalysis] = useState({
    guava: null,
    mexican: null,
    lemon: null
  });
  const [plantHistory, setPlantHistory] = useState([]);
  
  // Use localhost for the stream server
  const STREAM_URL = 'http://localhost:5000/video';
  const SENSOR_URL = 'http://192.168.31.163:5000/';
  const PLANTS_API_URL = 'http://192.168.31.163:9000/api/summary';
  const PLANT_ANALYSIS_API_URL = 'http://192.168.31.163:9000/api/plant-data';
  const PLANT_HISTORY_API_URL = 'http://192.168.31.163:9000/api/plant-data/history';
  
  // Dynamic plant details that use API data
  const getPlantDetails = () => ({
    guava: {
      title: 'Guava Plant',
      image: '/mango.png',
      leafImage: '/mango_analysis.png',
      description: 'The guava plant (Psidium guajava) is a tropical evergreen tree belonging to the Myrtaceae family, native to Central America but now cultivated throughout tropical and subtropical regions worldwide. This small to medium-sized tree typically grows 10-30 feet tall with oval to elliptic leaves that are dark green on top and lighter beneath, featuring prominent veins. The guava produces fragrant white flowers and round to pear-shaped fruits with green or yellow skin and sweet, flavorful flesh that ranges from white to pink and is rich in vitamin C, fiber, and antioxidants.',
      leftContent: [
        `Leaf Colour: ${plantData.guava.color}`,
        `Health Status: ${plantData.guava.status}`
      ],
      rightContent: [
        `Health Score: ${plantData.guava.health_score}`,
        `Issues: ${plantData.guava.issues}`
      ]
    },
    mexican: {
      title: 'Mexican Mint',
      image: '/mexican.png',
      leafImage: '/mexican_analysis.png',
      description: 'Cuban oregano (Plectranthus amboinicus), also known as Mexican mint or Indian borage. This herb features thick, succulent-like leaves covered in soft fuzz, with characteristic serrated or scalloped edges that form on sturdy stems. Cuban oregano is a member of the mint family and produces leaves with a distinctly spicy, aromatic fragrance when touched, making it popular for culinary use despite being unrelated to true oregano.',
      leftContent: [
        `Leaf Colour: ${plantData.mexican.color}`,
        `Health Status: ${plantData.mexican.status}`
      ],
      rightContent: [
        `Health Score: ${plantData.mexican.health_score}`,
        `Issues: ${plantData.mexican.issues}`
      ]
    },
    lemon: {
      title: 'Lemon Plant',
      image: '/lemon.png',
      leafImage: '/lemon_analysis.png',
      description: 'The lemon plant (Citrus × limon) is a small evergreen tree in the Rutaceae family that typically grows 10-20 feet tall with oval leaves that emerge reddish before turning dark green. This hybrid of citron and bitter orange produces fragrant white flowers and bright yellow oval fruits with a distinctive nipple-like protuberance, known for their highly acidic juice containing about 5-6% citric acid. Lemon trees require full sun (6-8 hours daily), well-drained moist soil, and regular feeding during the growing season, and can take 6 months or more for fruits to fully develop after flowering.',
      leftContent: [
        `Leaf Colour: ${plantData.lemon.color}`,
        `Health Status: ${plantData.lemon.status}`
      ],
      rightContent: [
        `Health Score: ${plantData.lemon.health_score}`,
        `Issues: ${plantData.lemon.issues}`
      ]
    }
  });
  
  const plantDetails = getPlantDetails();

  useEffect(() => {
    const img = document.getElementById('videoStream');
    if (img) {
      img.addEventListener('load', () => {
        setIsStreaming(true);
        setStreamError(null);
      });
      
      img.addEventListener('error', (e) => {
        setStreamError('Failed to load video stream. Make sure stream_server.py is running.');
        setIsStreaming(false);
        console.error('Video stream error:', e);
      });
    }
  }, []);

  // Fetch sensor value periodically
  useEffect(() => {
    const fetchSensorValue = async () => {
      try {
        const response = await fetch(SENSOR_URL);
        const data = await response.text();
        setSensorValue(data.trim());
      } catch (error) {
        console.error('Error fetching sensor value:', error);
        setSensorValue('Error');
      }
    };

    // Fetch immediately
    fetchSensorValue();

    // Then fetch every 500ms
    const interval = setInterval(fetchSensorValue, 500);

    return () => clearInterval(interval);
  }, []);

  // Fetch plant data from API
  useEffect(() => {
    const fetchPlantData = async () => {
      try {
        const response = await fetch(PLANTS_API_URL);
        const data = await response.json();
        
        // Check if plants_summary exists and is an array
        if (data.plants_summary && Array.isArray(data.plants_summary)) {
          // Map the API data to plant keys
          const newPlantData = {
            guava: {
              color: data.plants_summary[0]?.color || '-',
              status: data.plants_summary[0]?.status || '-',
              health_score: data.plants_summary[0]?.health_score !== undefined ? data.plants_summary[0].health_score.toString() : '-',
              issues: data.plants_summary[0]?.issues || '-'
            },
            mexican: {
              color: data.plants_summary[1]?.color || '-',
              status: data.plants_summary[1]?.status || '-',
              health_score: data.plants_summary[1]?.health_score !== undefined ? data.plants_summary[1].health_score.toString() : '-',
              issues: data.plants_summary[1]?.issues || '-'
            },
            lemon: {
              color: data.plants_summary[2]?.color || '-',
              status: data.plants_summary[2]?.status || '-',
              health_score: data.plants_summary[2]?.health_score !== undefined ? data.plants_summary[2].health_score.toString() : '-',
              issues: data.plants_summary[2]?.issues || '-'
            }
          };
          
          setPlantData(newPlantData);
        } else {
          // If no data available, keep the default '-' values
          console.log('No plant data available from API');
        }
      } catch (error) {
        console.error('Error fetching plant data:', error);
        // On error, keep the default '-' values
      }
    };

    // Fetch immediately
    fetchPlantData();

    // Then fetch every 2 seconds for real-time updates
    const interval = setInterval(fetchPlantData, 2000);

    return () => clearInterval(interval);
  }, []);

  // Fetch detailed plant analysis data
  useEffect(() => {
    const fetchPlantAnalysis = async () => {
      try {
        const response = await fetch(PLANT_ANALYSIS_API_URL);
        const data = await response.json();
        
        // Check if plants data exists and is an array
        if (data.plants && Array.isArray(data.plants)) {
          // Map the analysis data to plant keys
          const newPlantAnalysis = {
            guava: data.plants[0]?.analysis || null,
            mexican: data.plants[1]?.analysis || null,
            lemon: data.plants[2]?.analysis || null
          };
          
          setPlantAnalysis(newPlantAnalysis);
        }
      } catch (error) {
        console.error('Error fetching plant analysis:', error);
      }
    };

    // Fetch immediately
    fetchPlantAnalysis();

    // Then fetch every 2 seconds for real-time updates
    const interval = setInterval(fetchPlantAnalysis, 2000);

    return () => clearInterval(interval);
  }, []);

  // Fetch plant history for chart visualization
  useEffect(() => {
    const fetchPlantHistory = async () => {
      try {
        const response = await fetch(PLANT_HISTORY_API_URL);
        const data = await response.json();
        
        console.log('Plant history data:', data);
        
        // Check if history data exists - the API returns { data: [...] }
        if (data && data.data && Array.isArray(data.data)) {
          setPlantHistory(data.data);
        }
      } catch (error) {
        console.error('Error fetching plant history:', error);
      }
    };

    // Fetch immediately
    fetchPlantHistory();

    // Then fetch every 2 seconds for real-time updates
    const interval = setInterval(fetchPlantHistory, 2000);

    return () => clearInterval(interval);
  }, []);

  // Prepare chart data from plant history
  const prepareChartData = () => {
    if (!plantHistory || plantHistory.length === 0) {
      console.log('No plant history data available');
      return [];
    }

    // Map history data to chart format
    const chartData = plantHistory.map((item, index) => {
      const timestamp = item.cycle_timestamp ? new Date(item.cycle_timestamp).toLocaleTimeString() : `Time ${index}`;
      const guavaScore = item.plants?.[0]?.analysis?.overall_health?.score || 0;
      const mexicanScore = item.plants?.[1]?.analysis?.overall_health?.score || 0;
      const lemonScore = item.plants?.[2]?.analysis?.overall_health?.score || 0;
      
      return {
        timestamp,
        guava: guavaScore,
        mexican: mexicanScore,
        lemon: lemonScore
      };
    });

    console.log('Chart data prepared:', chartData);
    return chartData;
  };

  const chartData = prepareChartData();

  return (
    <>
      <div className="background-container">
        <PixelBlast 
          variant="circle"
          pixelSize={6}
          color="#9D7FEA"
          patternScale={3}
          patternDensity={1.2}
          pixelSizeJitter={0.5}
          enableRipples
          rippleSpeed={0.4}
          rippleThickness={0.12}
          rippleIntensityScale={1.5}
          liquid
          liquidStrength={0.12}
          liquidRadius={1.2}
          liquidWobbleSpeed={5}
          speed={0.6}
          edgeFade={0.25}
          transparent={false}
        />
      </div>
      <div className="app">
        <div className="main-content">
          <h1>Robotic Arm - Leaf Detection</h1>
          {selectedPlant ? (
            <div className="plant-detail-view">
              <button className="back-button" onClick={() => setSelectedPlant(null)}>
                ← Back to Plants
              </button>
                            <div className="empty-card">
                <div className="leaf-component-wrapper">
                  <LeafComponent
                    leftContent={plantDetails[selectedPlant].leftContent}
                    rightContent={plantDetails[selectedPlant].rightContent}
                    imageSrc={plantDetails[selectedPlant].leafImage}
                    imageAlt={`${plantDetails[selectedPlant].title} leaf details`}
                  />
                </div>
                {plantAnalysis[selectedPlant] && (
                  <div className="analysis-section-container">
                    <h2 className="analysis-title">Detailed Plant Analysis</h2>
                    <div className="analysis-content">
                      <div className="analysis-section">
                        <h3>Leaf Color Analysis</h3>
                        <p className="analysis-primary">{plantAnalysis[selectedPlant].leaf_color?.primary || '-'}</p>
                        <p className="analysis-description">{plantAnalysis[selectedPlant].leaf_color?.description || 'No data available'}</p>
                      </div>
                      <div className="analysis-section">
                        <h3>Leaf Condition</h3>
                        <p className="analysis-primary">{plantAnalysis[selectedPlant].leaf_condition?.status || '-'}</p>
                        <p className="analysis-description">{plantAnalysis[selectedPlant].leaf_condition?.description || 'No data available'}</p>
                      </div>
                      <div className="analysis-section">
                        <h3>Overall Health</h3>
                        <p className="analysis-primary">Score: {plantAnalysis[selectedPlant].overall_health?.score || '-'}</p>
                        <p className="analysis-description">{plantAnalysis[selectedPlant].overall_health?.description || 'No data available'}</p>
                      </div>
                      <div className="analysis-section">
                        <h3>Possible Issues</h3>
                        <p className="analysis-primary">Summary: {plantAnalysis[selectedPlant].possible_issues?.summary || '-'}</p>
                        {plantAnalysis[selectedPlant].possible_issues?.details && (
                          <ul className="analysis-list">
                            {plantAnalysis[selectedPlant].possible_issues.details.map((issue, index) => (
                              <li key={index}>{issue}</li>
                            ))}
                          </ul>
                        )}
                      </div>
                    </div>
                  </div>
                )}
                {chartData.length > 0 ? (
                  <div className="chart-section-container">
                    <h2 className="chart-title">Health Score History</h2>
                    <div className="chart-container">
                      <ResponsiveContainer width="100%" height={400}>
                        <LineChart data={chartData}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(157, 127, 234, 0.2)" />
                          <XAxis 
                            dataKey="timestamp" 
                            stroke="#9D7FEA"
                            style={{ fontSize: '12px' }}
                          />
                          <YAxis 
                            stroke="#9D7FEA"
                            style={{ fontSize: '12px' }}
                            domain={[0, 10]}
                            label={{ value: 'Health Score', angle: -90, position: 'insideLeft', style: { fill: '#9D7FEA' } }}
                          />
                          <Tooltip 
                            contentStyle={{ backgroundColor: 'rgba(0, 0, 0, 0.8)', border: '1px solid #9D7FEA', borderRadius: '8px' }}
                            labelStyle={{ color: '#9D7FEA' }}
                            itemStyle={{ color: '#fff' }}
                          />
                          <Legend wrapperStyle={{ color: '#fff' }} />
                          <Line type="monotone" dataKey="guava" stroke="#8884d8" strokeWidth={2} name="Guava" />
                          <Line type="monotone" dataKey="mexican" stroke="#82ca9d" strokeWidth={2} name="Mexican Mint" />
                          <Line type="monotone" dataKey="lemon" stroke="#ffc658" strokeWidth={2} name="Lemon" />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                ) : (
                  <div className="chart-section-container">
                    <h2 className="chart-title">Health Score History</h2>
                    <div className="chart-container">
                      <p style={{ color: '#ccc', textAlign: 'center', padding: '20px' }}>
                        No historical data available. Chart will appear once data is received from the API.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="cards-grid">
              <div className="card" onClick={() => setSelectedPlant('guava')}>
                <div className="card-content">
                  <div className="card-text-content">
                    <h2 className="card-title">Guava Plant</h2>
                    <p className="card-description">The guava plant (Psidium guajava) is a small evergreen tree or shrub in the Myrtaceae family, native to tropical America and now cultivated throughout tropical and subtropical regions worldwide. This plant typically grows 10-20 feet tall with distinctive four-angled young stems, oblong leaves measuring 3-7 inches in length with prominent veins and serrated margins, and fragrant white flowers about 1 inch in diameter featuring numerous stamens</p>
                  </div>
                  <img src="/mango.png" alt="Guava Plant" className="card-image" />
                </div>
              </div>
              <div className="card" onClick={() => setSelectedPlant('mexican')}>
                <div className="card-content">
                  <div className="card-text-content">
                    <h2 className="card-title">Mexican Mint</h2>
                    <p className="card-description">Cuban oregano (Plectranthus amboinicus), also known as Mexican mint or Indian borage. This herb features thick, succulent-like leaves covered in soft fuzz, with characteristic serrated or scalloped edges that form on sturdy stems. Cuban oregano is a member of the mint family and produces leaves with a distinctly spicy, aromatic fragrance when touched, making it popular for culinary use despite being unrelated to true oregano.</p>
                  </div>
                  <img src="/mexican.png" alt="Mexican Mint" className="card-image" />
                </div>
              </div>
              <div className="card card-centered" onClick={() => setSelectedPlant('lemon')}>
                <div className="card-content">
                  <div className="card-text-content">
                    <h2 className="card-title">Lemon Plant</h2>
                    <p className="card-description">The lemon plant (Citrus × limon) is a small evergreen tree in the Rutaceae family that typically grows 10-20 feet tall with oval leaves that emerge reddish before turning dark green. This hybrid of citron and bitter orange produces fragrant white flowers and bright yellow oval fruits with a distinctive nipple-like protuberance, known for their highly acidic juice containing about 5-6% citric acid. Lemon trees require full sun (6-8 hours daily), well-drained moist soil, and regular feeding during the growing season, and can take 6 months or more for fruits to fully develop after flowering.</p>
                  </div>
                  <img src="/lemon.png" alt="Lemon Plant" className="card-image" />
                </div>
              </div>
            </div>
          )}
        </div>
        
        <div className="video-container">
          <div className="video-wrapper">
            {streamError ? (
              <div className="error-message">
                <img src="/warning.png" alt="Warning" className="warning-image" />
                <p>Camera feed not available</p>
              </div>
            ) : (
              <img
                id="videoStream"
                src={STREAM_URL}
                alt="Leaf Detection Stream"
                className="video-stream"
              />
            )}
            <div className="sensor-display">
              <strong>Sensor Status:</strong> 
              <span className={`sensor-value ${sensorValue.toLowerCase()}`}>{sensorValue}</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
