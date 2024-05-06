import react from "react"
import "./SearchResultsList.css"
import { SearchResult } from "./SearchResult"

export const SearchResultsList = ({autoComplete, selectResult}) => {
    return (
        <div className="autocomplete-list">
            {autoComplete.map((autoComplete, id) => {
                return <SearchResult autocomplete={autoComplete} selectResult={selectResult} key={id}/>
            })}
        </div>
    )
}