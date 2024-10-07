import React, { useState } from "react";
import "../../styles/profile.css"


export const Profile = () => {
    const [activeTab, setActiveTab] = useState("preferences")

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
                <div className="tab-content mt-4">
                    {activeTab === 'preferences' && (
                        <div className="tab-pane">
                            <h5>Preferences</h5>
                            <p>Here you can set your preferences for the profile, notifications, etc.</p>
                        </div>
                    )}

                    {activeTab === 'restrictions' && (
                        <div className="tab-pane">
                            <h5>Restrictions</h5>
                            <p>Set any restrictions or limitations you'd like to apply.</p>
                        </div>
                    )}

                    {activeTab === 'favorites' && (
                        <div className="tab-pane">
                            <h5>Favorites</h5>
                            <p>Manage your favorite items, categories, and more.</p>
                        </div>
                    )}
                </div>

                {/* Tab content for each pill */}
                <div className="tab-content mt-4">
                    {activeTab === 'preferences' && (
                        <div className="tab-pane active">
                            <h5>Preferences</h5>
                            <p>Here you can set your preferences for the profile, notifications, etc.</p>
                        </div>
                    )}

                    {activeTab === 'restrictions' && (
                        <div className="tab-pane active">
                            <h5>Restrictions</h5>
                            <p>Set any restrictions or limitations you'd like to apply.</p>
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