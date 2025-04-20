import React, { useState } from 'react'
import PieChart from './PieChart'
import BarChart from './BarChart'

const ChartContainer = ({ fileId }) => {
    const [chartType, setChartType] = useState('pie')

    return (
        <div>
            <div style={{ marginBottom: '20px' }}>
                <button 
                    onClick={() => setChartType('pie')}
                    className={`waves-effect waves-light btn ${chartType === 'pie' ? 'purple' : 'grey'}`}
                    style={{ marginRight: '10px' }}
                >
                    Pie Chart
                </button>
                <button 
                    onClick={() => setChartType('bar')}
                    className={`waves-effect waves-light btn ${chartType === 'bar' ? 'purple' : 'grey'}`}
                >
                    Bar Chart
                </button>
            </div>
            {chartType === 'pie' ? (
                <PieChart fileId={fileId} />
            ) : (
                <BarChart fileId={fileId} />
            )}
        </div>
    )
}

export default ChartContainer