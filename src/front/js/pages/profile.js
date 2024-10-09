import React, { useState, useEffect } from "react";
import "../../styles/profile.css"
import ToggleSwitch from '../component/ToggleSwitch';

const foodRestrictons = [
    "dairy", "eggs", "fish", "shellfish", "wheat", "soybeans",
    "sesame", "tree nuts", "peanuts", "pork", "beef"
]
const foodPreferences = [
    "dairy", "eggs", "fish", "shellfish", "wheat", "soybeans",
    "sesame", "tree nuts", "peanuts", "pork", "beef"
]


export const Profile = () => {
    const [activeTab, setActiveTab] = useState("preferences")
    const [restrictions, setRestrictions] = useState({});

    const handleToggle = (restriction) => {
        setRestrictions(prev => ({
            ...prev,
            [restriction]: !prev[restriction]
        }));
    };

    const handleSave = async () => {
        console.log("saving preferences:", restrictions);
        alert("preferences saved successfully!");
    }
    return (
        <>
            <div className="container profile-page-top-div">
                <h3>Profile page tbc</h3>

            </div>
            <div className="container profile-page-div">
                <ul className="nav nav-pills nav-fill">
                    <li className="nav-item">
                        <a
                            className={`nav-link ${activeTab === "preferences" ? "active" : ""}`}
                            onClick={() => setActiveTab("preferences")}
                            href="#">
                            Preferences
                        </a>
                    </li>
                    <li className={`nav-link ${activeTab === "restrictions" ? "active" : ""}`}>
                        <a
                            className="nav-link"
                            onClick={() => setActiveTab("restrictions")}
                            href="#">
                            Restrictions
                        </a>
                    </li>
                    <li className={`nav-link ${activeTab === "favorites" ? "active" : ""}`}>
                        <a
                            className="nav-link"
                            onClick={() => setActiveTab("favorites")}
                            href="#">
                            Favorites
                        </a>
                    </li>
                </ul>
                {/* <div className="tab-content mt-4">
                    {activeTab === 'preferences' && (
                        <div className="tab-pane">
                            <h5>Preferences</h5>
                            <p>Here you can set your preferences for the profile, notifications, etc.</p>
                        </div>
                    )}

                    {activeTab === 'restrictions' && (
                        <div className="tab-pane">
                            <h5 className="card-title mb-4 text-center">Restrictions</h5>
                            <p>Set any restrictions you'd like to apply.</p>
                        </div>
                    )}

                    {activeTab === 'favorites' && (
                        <div className="tab-pane">
                            <h5>Favorites</h5>
                            <p>Manage your favorite items, categories, and more.</p>
                        </div>
                    )}
                </div> */}

                {/* Tab content for each pill */}
                <div className="tab-content mt-4">
                    {activeTab === 'preferences' && (
                        <div className="tab-pane active d-flex justify-content-center align-items-center flex-column">
                            <h5 className="mb-4 text-center">Preferences</h5>
                            <div className="row w-50">
                                {foodPreferences.map((preference) => (
                                    <div key={preference} className="col-md-6 mb-3 d-flex justify-content-center">
                                        <div className="d-flex align-item-center justify-content-between border rounded p-2 w-100">
                                            <span className="text-capitalize">
                                                {preference}
                                            </span>
                                            {/* <div
                                                className={`btn btn-sm ${restrictions[restriction] ? "btn-primary" : "btn-outline-primary"}`}
                                                onClick={() => handleToggle(restriction)}
                                            >

                                            </div> */}
                                            <ToggleSwitch
                                                isOn={restrictions[preference] || false}
                                                onToggle={() => handleToggle(preference)}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <button onClick={handleSave} className="btn btn-primary mt-3 mb-2">
                                <i className="fa-solid fa-cloud me-2"></i>
                                Save Preferences
                            </button>
                        </div>
                    )}

                    {activeTab === 'restrictions' && (
                        <div className="tab-pane active d-flex justify-content-center align-items-center flex-column">
                            <h5 className="mb-4 text-center">Restrictions</h5>
                            <div className="row w-50">
                                {foodRestrictons.map((restriction) => (
                                    <div key={restriction} className="col-md-6 mb-3 d-flex justify-content-center">
                                        <div className="d-flex align-items-center justify-content-between border rounded p-2 w-100">
                                            <span className="text-capitalize">
                                                {restriction}
                                            </span>
                                            {/* <div
                                                className={`btn btn-sm ${restrictions[restriction] ? "btn-primary" : "btn-outline-primary"}`}
                                                onClick={() => handleToggle(restriction)}
                                            >

                                            </div> */}
                                            <ToggleSwitch
                                                isOn={restrictions[restriction] || false}
                                                onToggle={() => handleToggle(restriction)}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <button onClick={handleSave} className="btn btn-primary mt-3 mb-2">
                                <i className="fa-solid fa-cloud me-2"></i>
                                Save Restrictions
                            </button>
                        </div>
                    )}

                    {activeTab === 'favorites' && (
                        <div className="tab-pane active">
                            <h5>Favorites</h5>
                            <p>Manage your favorite items, categories, and more.</p>
                        </div>
                    )}
                </div>


            </div>
        </>

    )

}


//  saved version of user profile 2