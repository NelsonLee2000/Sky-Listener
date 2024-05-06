import React from "react";
import "./SearchResult.css"

export const SearchResult = ({autocomplete, selectResult}) => {
    return (
        <div className="search-result" onClick={(e) => selectResult(autocomplete)}>{autocomplete}</div>
    )
}