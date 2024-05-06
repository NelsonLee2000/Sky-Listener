import React from "react";
import "./App.css";
import axios from "axios";
import { useState, useEffect } from "react";
import search_icon from "./Assets/search.png";
import { SearchResultsList } from "./components/SearchResultsList";

function App() {
  const [error, setError] = useState("");
  const [city, setCity] = useState("");
  const [surl, setSurl] = useState("");
  const [siconUrl, setSiconUrl] = useState("");
  const [title, setTitle] = useState("");
  const [wicon, setWicon] = useState("");
  const [wtitle, setWtitle] = useState("");
  const [temp, setTemp] = useState("");
  const [autoComplete, setAutoComplete] = useState([]);

  const onChange = (e) => {
    setError("");
    setCity(e.target.value);
  };

  useEffect(() => {
    if (city) {
      fetchAutoComplete(city);
    }
  }, [city]);

  const selectResult = (select) => {
    setCity(select);
  };

  async function fetchAutoComplete(input) {

    if (input.includes("/") || input.includes("\\")) {
      return
    }
    else {
      const { data } = await axios.get(
        `https://sky-listener.onrender.com/auto-complete/${input}`
      );
      setAutoComplete(data);
    }
  }

  async function fetchPlaylist(city) {
    return await axios.get(`https://sky-listener.onrender.com/get-weather/${city}`);
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await fetchPlaylist(city);
      if ("error" in data) {
        setError(data.error);
      } else {
        setError("");
        const kelvinTemperature = data.response.main.temp;
        const celsiusTemperature = kelvinTemperature - 273.15;
        setWicon(
          `https://openweathermap.org/img/wn/${data.response.weather[0].icon}@2x.png`
        );
        setTemp(celsiusTemperature.toFixed(0) + "°C");
        setWtitle(`${data.response.name}, ${data.response.sys.country}`);
        setSurl(data.playlists[0].external_urls.spotify);
        setTitle(data.playlists[0].name);
        setSiconUrl(data.playlists[0].images[0].url);
      }
      setAutoComplete([]);
    } catch (err) {
      console.log(err.message);
    }
  };

  return (
    <div className="App">
      <h1 className="title">Sky Listener</h1>
      <div className="search-bar-container">
        <form onSubmit={onSubmit} className="form">
          <input
            type="text"
            value={city}
            onChange={(e) => onChange(e)}
            className="searchinput"
            placeholder="Search a City"
          ></input>
          <button type="submit" className="searchbutton">
            <i className="fa-solid fa-magnifying-glass" id="search-icon"></i>
          </button>
        </form>
        {autoComplete && autoComplete.length > 0 && city && <SearchResultsList autoComplete={autoComplete} selectResult={selectResult} />}
      </div>
      <div className="error">{error}</div>
      {temp === "" ? (
        <div className="nosearch">
          Search for your city, and you'll be recommended a weather-appropriate
          Spotify playlist!
        </div>
      ) : (
        <div className="mainbody">
          <div className="wdiv">
            <div className="city">{wtitle}</div>
            <img src={wicon} className="wicon"></img>
            <div className="temp">{temp}</div>
          </div>
          <div className="sdiv">
            <div className="playlisttitle">{title}</div>
            <div>
              <img
                src={siconUrl}
                alt="Playlist Icon"
                className="playlistimage"
              />
            </div>
            <div>
              <a href={surl} className="playlistlink" target="_blank">
                {surl}
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
