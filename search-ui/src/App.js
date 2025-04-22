import React, { useEffect, useState } from 'react';
import "./App.css"

function App() {
    const [currPage, setCurrPage] = useState(0)
    const [maxPages, setMaxPages] = useState(0)
    const [results, setResults] = useState([])
    const [inputValues, setInputValues] = useState({
        'generated_text': '',
        'duration': '',
        'age': '',
        'gender': '',
        'accent': ''
    })

    const nextPage = () => {
        if (currPage < maxPages-1){
            setCurrPage(currPage + 1)
        }
    }

    const prevPage = () => {
        if (currPage > 0){
            setCurrPage(currPage - 1)
        }
    }

    const computeMaxPages = (num_results, num_results_per_page) => {
        let base = Math.floor(num_results / num_results_per_page)

        if(num_results % num_results_per_page > 0){
            base = base + 1
        }

        return base
    }

    const updateInputValues = (e) => {
        const {name, value} = e.target

        setInputValues({
            ...inputValues,
            [name]: value
        })
    }

    const submitFilters = async () => {
        const response = await fetch('http://3.25.54.197:9200/cv-transcriptions/_search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "query": {
                    "bool": {
                        'must': Object.keys(inputValues).filter(field => inputValues[field] != "").map((field) => ({
                            match: {
                                [field]: inputValues[field]
                            }
                        }))
                    }
                },
                "size": 1000
            })
        })
        
        const data = await response.json()
        setResults(data.hits.hits)
        setCurrPage(0)
        setMaxPages(computeMaxPages(data.hits.hits.length, 3))
    }

  return (
    <div className="App">
        <div className='main'>
            <div className='filters'>
                <h3>Filters</h3>
                <div className='form-input'>
                    <label>
                        Generated Text: <br/><input name='generated_text' onChange={updateInputValues} /><br/>
                    </label>
                </div>
                <div className='form-input'>
                    <label>
                        Duration: <br/><input name='duration' onChange={updateInputValues} /><br/>
                    </label>
                </div>
                <div className='form-input'>
                    <label>
                        Age: <br/><input name='age' onChange={updateInputValues} /><br/>
                    </label>
                </div>
                <div className='form-input'>
                    <label>
                        Gender: <br/><input name='gender' onChange={updateInputValues} /><br/>
                    </label>
                </div>
                <div className='form-input'>
                    <label>
                        Accent: <br/><input name='accent' onChange={updateInputValues} /><br/>
                    </label>
                </div>
                <button onClick={submitFilters}>Filter</button>
            </div>
            <div className='results'>
                <h3>Results</h3>
                {results.length == 0 ? 
                    <p>Please enter a search query</p> : 
                    <>
                        {results.slice(currPage*3, (currPage*3)+3).map((item) => {
                            return (<div className='result-cell'>
                                <p>Generated Text: {item._source.generated_text}</p>
                                <p>Duration: {item._source.duration}</p>
                                <p>Age: {item._source.age}</p>
                                <p>Accent: {item._source.accent}</p>
                                <p>Gender: {item._source.gender}</p>
                            </div>)
                        })}
                        <div className='pagination'>
                            <button className='leftBtn' onClick={prevPage}>Previous Page</button>
                            <p>Page {currPage+1} of {maxPages}</p>
                            <button className='rightBtn' onClick={nextPage}>Next Page</button>
                        </div>
                    </>
                }
            </div>
        </div>
    </div>
  );
}

export default App;