from flask import Flask, render_template_string, request, jsonify
import os
import json
import urllib.request
import urllib.error

app = Flask(__name__)

# ============================================================
# DESTINATION DATA
# ============================================================

DESTINATIONS = [
    {"name":"Finland","country":"Finland","region":"Europe","image":"https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=85","description":"Experience northern lights, peaceful lakes, snowy landscapes and Scandinavian culture.","rating":4.9,"tags":["Northern Lights","Nature","Snow"],"price":"₹1.2L+"},
    {"name":"Paris","country":"France","region":"Europe","image":"https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=85","description":"Explore iconic landmarks, art, cafés, fashion and romantic streets.","rating":4.8,"tags":["Romantic","Culture","Food"],"price":"₹90K+"},
    {"name":"Tokyo","country":"Japan","region":"Asia","image":"https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=85","description":"A futuristic city combining technology, traditional culture and incredible food.","rating":4.9,"tags":["Technology","Food","Culture"],"price":"₹1L+"},
    {"name":"Goa","country":"India","region":"India","image":"https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=85","description":"Relax on beaches, explore Portuguese architecture and enjoy vibrant nightlife.","rating":4.7,"tags":["Beach","Nightlife","Food"],"price":"₹20K+"},
    {"name":"Ooty","country":"India","region":"India","image":"https://images.unsplash.com/photo-1593693411515-c20261bcad6e?auto=format&fit=crop&w=1200&q=85","description":"Enjoy cool weather, tea gardens, mountains and peaceful scenic views.","rating":4.6,"tags":["Mountains","Nature","Relax"],"price":"₹12K+"},
    {"name":"Dubai","country":"UAE","region":"Middle East","image":"https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=85","description":"Discover luxury shopping, desert adventures, skyscrapers and world-class attractions.","rating":4.8,"tags":["Luxury","Shopping","Adventure"],"price":"₹70K+"},
    {"name":"Bali","country":"Indonesia","region":"Asia","image":"https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=85","description":"Tropical beaches, temples, waterfalls and relaxing island experiences.","rating":4.8,"tags":["Beach","Adventure","Relax"],"price":"₹55K+"},
    {"name":"Swiss Alps","country":"Switzerland","region":"Europe","image":"https://images.unsplash.com/photo-1531366936337-7c912a4589a7?auto=format&fit=crop&w=1200&q=85","description":"Snow-covered mountains, scenic trains and unforgettable alpine landscapes.","rating":4.9,"tags":["Snow","Mountains","Luxury"],"price":"₹1.5L+"},
    {"name":"Singapore","country":"Singapore","region":"Asia","image":"https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=85","description":"Modern architecture, gardens, shopping and diverse Asian cuisine.","rating":4.8,"tags":["City","Food","Family"],"price":"₹60K+"},
    {"name":"Maldives","country":"Maldives","region":"Asia","image":"https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=85","description":"Crystal-clear waters, private beaches and beautiful island resorts.","rating":4.9,"tags":["Beach","Luxury","Couple"],"price":"₹80K+"},
    {"name":"Kyoto","country":"Japan","region":"Asia","image":"https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=85","description":"Discover temples, gardens, traditional streets and beautiful Japanese culture.","rating":4.9,"tags":["Culture","Nature","Food"],"price":"₹95K+"},
    {"name":"Seoul","country":"South Korea","region":"Asia","image":"https://images.unsplash.com/photo-1538485399081-7c897e6f5e8d?auto=format&fit=crop&w=1200&q=85","description":"Enjoy K-culture, modern neighbourhoods, palaces, shopping and Korean food.","rating":4.8,"tags":["City","Food","Shopping"],"price":"₹85K+"},
    {"name":"Hong Kong","country":"Hong Kong","region":"Asia","image":"https://images.unsplash.com/photo-1536599018102-9f803c140fc1?auto=format&fit=crop&w=1200&q=85","description":"A vibrant city of skyscrapers, harbour views, markets and amazing cuisine.","rating":4.7,"tags":["City","Food","Shopping"],"price":"₹75K+"},
    {"name":"Baku","country":"Azerbaijan","region":"Caucasus","image":"https://images.unsplash.com/photo-1539650116574-75c0c6d73f6e?auto=format&fit=crop&w=1200&q=85","description":"Explore the Caspian coast, old city lanes, modern architecture and local food.","rating":4.6,"tags":["Culture","City","Food"],"price":"₹55K+"},
    {"name":"Tbilisi","country":"Georgia","region":"Caucasus","image":"https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=1200&q=85","description":"Wander historic streets, sulphur baths, mountain viewpoints and lively cafés.","rating":4.7,"tags":["Culture","Food","Nature"],"price":"₹60K+"},
    {"name":"Prague","country":"Czech Republic","region":"Europe","image":"https://images.unsplash.com/photo-1519677100203-a0e668c92439?auto=format&fit=crop&w=1200&q=85","description":"See fairy-tale architecture, historic squares, bridges and charming cafés.","rating":4.8,"tags":["Culture","Romantic","Photography"],"price":"₹85K+"},
    {"name":"Vienna","country":"Austria","region":"Europe","image":"https://images.unsplash.com/photo-1516550893923-42d28e5677af?auto=format&fit=crop&w=1200&q=85","description":"Enjoy imperial palaces, classical music, elegant cafés and beautiful parks.","rating":4.8,"tags":["Culture","Food","Romantic"],"price":"₹95K+"},
    {"name":"Lisbon","country":"Portugal","region":"Europe","image":"https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1200&q=85","description":"Explore colourful streets, viewpoints, historic trams and Portuguese cuisine.","rating":4.8,"tags":["Food","Culture","Photography"],"price":"₹90K+"},
    {"name":"Reykjavik","country":"Iceland","region":"Europe","image":"https://images.unsplash.com/photo-1504893524553-b855bce32c67?auto=format&fit=crop&w=1200&q=85","description":"Use Reykjavik as a base for waterfalls, glaciers, geothermal pools and northern lights.","rating":4.9,"tags":["Nature","Adventure","Northern Lights"],"price":"₹1.4L+"},
    {"name":"Copenhagen","country":"Denmark","region":"Europe","image":"https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?auto=format&fit=crop&w=1200&q=85","description":"Discover colourful harbour streets, cycling culture, design and Nordic cuisine.","rating":4.8,"tags":["City","Food","Culture"],"price":"₹1.1L+"},
    {"name":"Athens","country":"Greece","region":"Europe","image":"https://images.unsplash.com/photo-1603565816030-6b389eeb23cb?auto=format&fit=crop&w=1200&q=85","description":"Visit ancient landmarks, lively neighbourhoods and enjoy Greek food by the sea.","rating":4.7,"tags":["History","Food","Culture"],"price":"₹85K+"},
    {"name":"Vancouver","country":"Canada","region":"North America","image":"https://images.unsplash.com/photo-1559511260-66a654ae982a?auto=format&fit=crop&w=1200&q=85","description":"Combine a modern waterfront city with mountains, parks and outdoor adventures.","rating":4.8,"tags":["Nature","Adventure","City"],"price":"₹1.3L+"},
    {"name":"San Francisco","country":"USA","region":"North America","image":"https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1200&q=85","description":"Explore iconic bridges, waterfront neighbourhoods, viewpoints and diverse food.","rating":4.7,"tags":["City","Food","Photography"],"price":"₹1.5L+"},
    {"name":"Honolulu","country":"USA","region":"North America","image":"https://images.unsplash.com/photo-1507876466751-8a2a0be4f1a2?auto=format&fit=crop&w=1200&q=85","description":"Enjoy tropical beaches, island culture, scenic hikes and ocean adventures.","rating":4.8,"tags":["Beach","Nature","Adventure"],"price":"₹1.6L+"},
    {"name":"Mexico City","country":"Mexico","region":"North America","image":"https://images.unsplash.com/photo-1518659526054-190340b32735?auto=format&fit=crop&w=1200&q=85","description":"Experience museums, historic districts, colourful markets and outstanding Mexican cuisine.","rating":4.7,"tags":["Food","Culture","City"],"price":"₹1L+"},
    {"name":"Seychelles","country":"Seychelles","region":"Africa","image":"https://images.unsplash.com/photo-1589979481223-deb893043163?auto=format&fit=crop&w=1200&q=85","description":"Relax on pristine beaches, swim in clear waters and explore tropical islands.","rating":4.9,"tags":["Beach","Luxury","Couple"],"price":"₹1.3L+"},
    {"name":"Zanzibar","country":"Tanzania","region":"Africa","image":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=1200&q=85","description":"Discover spice markets, historic Stone Town and beautiful Indian Ocean beaches.","rating":4.7,"tags":["Beach","Culture","Adventure"],"price":"₹1.1L+"},
    {"name":"Mauritius","country":"Mauritius","region":"Africa","image":"https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?auto=format&fit=crop&w=1200&q=85","description":"Enjoy lagoons, mountain views, island adventures and relaxing resort stays.","rating":4.8,"tags":["Beach","Relax","Adventure"],"price":"₹1.1L+"},
    {"name":"Buenos Aires","country":"Argentina","region":"South America","image":"https://images.unsplash.com/photo-1589909202802-8f4aadce1849?auto=format&fit=crop&w=1200&q=85","description":"Explore grand avenues, tango culture, neighbourhood cafés and Argentine cuisine.","rating":4.7,"tags":["Culture","Food","Nightlife"],"price":"₹1.3L+"},
    {"name":"Auckland","country":"New Zealand","region":"Oceania","image":"https://images.unsplash.com/photo-1507699622108-4be3abd695ad?auto=format&fit=crop&w=1200&q=85","description":"Enjoy harbour views, volcanic landscapes, beaches and easy outdoor adventures.","rating":4.8,"tags":["Nature","Adventure","City"],"price":"₹1.4L+"},
    {"name":"London","country":"United Kingdom","region":"Europe","image":"https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=85","description":"See royal landmarks, museums, markets, theatre and classic British neighbourhoods.","rating":4.8,"tags":["Culture","Shopping","Food"],"price":"₹1.2L+"},
    {"name":"Rome","country":"Italy","region":"Europe","image":"https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=1200&q=85","description":"Walk through ancient ruins, grand piazzas, art treasures and authentic Italian restaurants.","rating":4.9,"tags":["History","Food","Culture"],"price":"₹1L+"},
    {"name":"Barcelona","country":"Spain","region":"Europe","image":"https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1200&q=85","description":"Enjoy Gaudi architecture, beaches, tapas, markets and lively city streets.","rating":4.8,"tags":["Beach","Food","Culture"],"price":"₹95K+"},
    {"name":"Amsterdam","country":"Netherlands","region":"Europe","image":"https://images.unsplash.com/photo-1534351590666-13e3e96b5017?auto=format&fit=crop&w=1200&q=85","description":"Cruise canals, visit museums, explore charming streets and enjoy Dutch cafés.","rating":4.8,"tags":["Culture","Photography","Food"],"price":"₹1L+"},
    {"name":"Istanbul","country":"Turkey","region":"Europe","image":"https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1200&q=85","description":"Cross continents through historic mosques, bazaars, Bosphorus views and Turkish cuisine.","rating":4.8,"tags":["Culture","Food","Shopping"],"price":"₹75K+"},
    {"name":"Cairo","country":"Egypt","region":"Africa","image":"https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?auto=format&fit=crop&w=1200&q=85","description":"Discover pyramids, ancient history, Nile views and vibrant Egyptian markets.","rating":4.7,"tags":["History","Culture","Adventure"],"price":"₹80K+"},
    {"name":"Cape Town","country":"South Africa","region":"Africa","image":"https://images.unsplash.com/photo-1580060839134-75a5edca2e99?auto=format&fit=crop&w=1200&q=85","description":"Combine dramatic mountains, beaches, scenic drives, food and outdoor experiences.","rating":4.9,"tags":["Nature","Adventure","Food"],"price":"₹1.1L+"},
    {"name":"Sydney","country":"Australia","region":"Oceania","image":"https://images.unsplash.com/photo-1506973035872-a4a23b4e6b8d?auto=format&fit=crop&w=1200&q=85","description":"Enjoy harbour landmarks, beaches, coastal walks, dining and city experiences.","rating":4.8,"tags":["Beach","City","Adventure"],"price":"₹1.5L+"},
    {"name":"Melbourne","country":"Australia","region":"Oceania","image":"https://images.unsplash.com/photo-1514395462725-fb4566210144?auto=format&fit=crop&w=1200&q=85","description":"Explore laneways, coffee culture, art, sports and diverse restaurants.","rating":4.7,"tags":["Food","Culture","City"],"price":"₹1.5L+"},
    {"name":"Bangkok","country":"Thailand","region":"Asia","image":"https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=85","description":"Enjoy temples, street food, markets, river views and energetic nightlife.","rating":4.7,"tags":["Food","Shopping","Nightlife"],"price":"₹50K+"},
    {"name":"Phuket","country":"Thailand","region":"Asia","image":"https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?auto=format&fit=crop&w=1200&q=85","description":"Relax on tropical beaches, island-hop and enjoy water activities and sunsets.","rating":4.8,"tags":["Beach","Adventure","Relax"],"price":"₹55K+"},
    {"name":"Kuala Lumpur","country":"Malaysia","region":"Asia","image":"https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1200&q=85","description":"See modern towers, lively markets, shopping districts and Malaysian food.","rating":4.7,"tags":["City","Food","Shopping"],"price":"₹45K+"},
    {"name":"Kathmandu","country":"Nepal","region":"Asia","image":"https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=85","description":"Explore temples, Himalayan views, heritage squares and mountain adventures.","rating":4.7,"tags":["Mountains","Culture","Adventure"],"price":"₹35K+"},
    {"name":"Manali","country":"India","region":"India","image":"https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=85","description":"Enjoy Himalayan scenery, cafés, river views, snow and outdoor activities.","rating":4.7,"tags":["Mountains","Adventure","Nature"],"price":"₹18K+"},
    {"name":"Jaipur","country":"India","region":"India","image":"https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1200&q=85","description":"Discover royal forts, colourful markets, palaces and famous Rajasthani cuisine.","rating":4.8,"tags":["Culture","History","Food"],"price":"₹15K+"},
    {"name":"Kerala","country":"India","region":"India","image":"https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=85","description":"Relax through backwaters, beaches, hill stations, local food and wellness experiences.","rating":4.8,"tags":["Nature","Relax","Food"],"price":"₹20K+"},
    {"name":"Andaman Islands","country":"India","region":"India","image":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85","description":"Experience clear water, island beaches, coral reefs and peaceful tropical escapes.","rating":4.8,"tags":["Beach","Adventure","Relax"],"price":"₹30K+"},
    {"name":"Darjeeling","country":"India","region":"India","image":"https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=85","description":"Enjoy tea gardens, Himalayan views, toy-train rides and cool mountain weather.","rating":4.7,"tags":["Mountains","Nature","Relax"],"price":"₹16K+"},
    {"name":"Munnar","country":"India","region":"India","image":"https://images.unsplash.com/photo-1605640840605-14ac1855827b?auto=format&fit=crop&w=1200&q=85","description":"Explore rolling tea estates, waterfalls, misty hills and peaceful nature trails.","rating":4.7,"tags":["Nature","Mountains","Photography"],"price":"₹15K+"},
    {"name":"Pondicherry","country":"India","region":"India","image":"https://images.unsplash.com/photo-1602643163983-ed0babc39797?auto=format&fit=crop&w=1200&q=85","description":"Enjoy French-colonial streets, cafés, beaches, cycling and a relaxed coastal vibe.","rating":4.6,"tags":["Beach","Food","Relax"],"price":"₹12K+"}
]


# ============================================================
# HTML
# ============================================================

HTML = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Voyanta AI Travel Planner</title>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Inter, Arial, sans-serif;
    background: #f7f8f5;
    color: #17231d;
}

button,
input {
    font-family: inherit;
}

button {
    cursor: pointer;
}

.navbar {
    height: 78px;
    background: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6%;
    border-bottom: 1px solid #e8ece8;
    position: sticky;
    top: 0;
    z-index: 20;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: #174d38;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
}

.brand-name {
    font-size: 22px;
    font-weight: 800;
    color: #173f30;
}

.brand-sub {
    font-size: 9px;
    letter-spacing: 2px;
    color: #829087;
    margin-top: 2px;
}

.nav-links {
    display: flex;
    gap: 35px;
}

.nav-links button {
    border: none;
    background: none;
    color: #66736c;
    font-size: 14px;
    padding: 8px;
}

.nav-links button:hover,
.nav-links .active {
    color: #174d38;
    font-weight: 700;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.icon-button {
    border: none;
    background: #f4f6f3;
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.profile {
    display: flex;
    align-items: center;
    gap: 9px;
}

.avatar {
    width: 39px;
    height: 39px;
    border-radius: 50%;
    background: #dce9e0;
    color: #174d38;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 800;
}

.profile strong {
    display: block;
    font-size: 13px;
}

.profile span {
    font-size: 11px;
    color: #8a948e;
}

.hero {
    min-height: 490px;
    background:
        linear-gradient(90deg, rgba(10,38,26,.9), rgba(10,38,26,.42)),
        url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=90");
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    padding: 70px 8%;
}

.hero-content {
    max-width: 730px;
    color: white;
}

.hero-badge {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    background: rgba(255,255,255,.14);
    border: 1px solid rgba(255,255,255,.25);
    padding: 9px 15px;
    border-radius: 30px;
    font-size: 12px;
    margin-bottom: 22px;
}

.hero h1 {
    font-size: clamp(42px, 6vw, 70px);
    line-height: 1.02;
    letter-spacing: -3px;
}

.hero h1 span {
    color: #b7d9bd;
}

.hero p {
    max-width: 620px;
    margin: 25px 0;
    line-height: 1.7;
    color: #e3ece5;
}

.search-box {
    background: white;
    width: min(650px, 100%);
    padding: 8px 15px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #647168;
}

.search-box input {
    border: none;
    outline: none;
    flex: 1;
    font-size: 15px;
    padding: 13px 3px;
}

.search-box button {
    border: none;
    background: none;
}

.quick-searches {
    margin-top: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    font-size: 12px;
}

.quick-searches button {
    border: 1px solid rgba(255,255,255,.35);
    background: rgba(255,255,255,.08);
    color: white;
    border-radius: 20px;
    padding: 6px 12px;
}

.content {
    padding: 70px 7%;
}

.section-heading {
    display: flex;
    justify-content: space-between;
    align-items: end;
    margin-bottom: 30px;
}

.section-heading h2 {
    font-size: 31px;
    margin-top: 7px;
}

.eyebrow {
    font-size: 10px;
    letter-spacing: 2px;
    color: #4f8065;
    font-weight: 800;
}

.result-count {
    color: #7b877f;
    font-size: 13px;
}

.destination-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}

.destination-card {
    background: white;
    border: 1px solid #e6ebe6;
    border-radius: 19px;
    overflow: hidden;
    transition: .25s;
}

.destination-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(28,57,42,.10);
}

.destination-image {
    height: 235px;
    position: relative;
}

.destination-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.save-button {
    position: absolute;
    top: 14px;
    right: 14px;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: none;
    background: white;
    color: #405148;
    display: flex;
    align-items: center;
    justify-content: center;
}

.save-button.saved {
    color: #b74d55;
}

.image-region {
    position: absolute;
    bottom: 13px;
    left: 13px;
    color: white;
    font-size: 11px;
    background: rgba(0,0,0,.45);
    padding: 6px 10px;
    border-radius: 20px;
}

.destination-info {
    padding: 20px;
}

.destination-title-row {
    display: flex;
    justify-content: space-between;
}

.destination-info h3 {
    font-size: 21px;
}

.destination-info p {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #829087;
    font-size: 12px;
    margin-top: 5px;
}

.rating {
    display: flex;
    gap: 4px;
    align-items: center;
    color: #b37b24;
    font-size: 12px;
}

.destination-description {
    line-height: 1.6;
    min-height: 57px;
}

.tag-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin: 15px 0;
}

.tag-row span {
    background: #edf4ee;
    color: #41604d;
    padding: 6px 9px;
    border-radius: 8px;
    font-size: 10px;
}

.card-footer {
    border-top: 1px solid #edf0ed;
    padding-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #7b877f;
    font-size: 12px;
}

.card-footer strong {
    color: #173f30;
}

.features-section {
    background: white;
    padding: 75px 7%;
}

.centered {
    display: block;
    text-align: center;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 40px;
}

.feature-card {
    padding: 28px;
    border: 1px solid #e5ebe5;
    border-radius: 17px;
}

.feature-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #e9f2eb;
    color: #174d38;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 18px;
}

.feature-card h3 {
    font-size: 16px;
    margin-bottom: 9px;
}

.feature-card p {
    color: #78847c;
    font-size: 13px;
    line-height: 1.6;
}

.footer {
    background: #123528;
    color: white;
    padding: 40px 7%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.footer .brand-name {
    color: white;
}

.footer p,
.footer span {
    color: #aec1b4;
    font-size: 12px;
}

/* =========================================================
   DESTINATION PAGE
========================================================= */

.page-header {
    padding: 20px 7%;
    background: white;
    display: flex;
    justify-content: space-between;
}

.back-button {
    border: none;
    background: #f0f4f0;
    padding: 10px 15px;
    border-radius: 10px;
    color: #355344;
}

.destination-hero {
    height: 470px;
    position: relative;
    overflow: hidden;
}

.destination-hero img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.destination-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(transparent 20%, rgba(8,30,20,.9));
    display: flex;
    align-items: end;
    padding: 7%;
    color: white;
}

.destination-overlay h1 {
    font-size: 65px;
    letter-spacing: -3px;
}

.destination-overlay p {
    max-width: 650px;
    line-height: 1.6;
    margin: 10px 0;
}

.hero-location {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
}

.hero-rating {
    display: flex;
    gap: 7px;
    align-items: center;
    font-size: 13px;
}

.details-content {
    padding: 65px 7%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
}

.details-main h2 {
    font-size: 37px;
    margin: 10px 0;
}

.large-text {
    font-size: 16px;
    line-height: 1.8;
    color: #728078;
}

.interest-preview {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 25px 0;
}

.interest-preview span {
    background: #eaf2eb;
    color: #355c46;
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 12px;
    display: flex;
    gap: 5px;
    align-items: center;
}

.primary-button {
    background: #174d38;
    color: white;
    border: none;
    padding: 14px 20px;
    border-radius: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 9px;
}

.primary-button:hover {
    background: #0e3928;
}

.primary-button.large {
    padding: 16px 23px;
}

.info-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.info-card {
    background: white;
    border: 1px solid #e5ebe5;
    border-radius: 15px;
    padding: 20px;
    display: flex;
    gap: 15px;
}

.info-icon {
    min-width: 42px;
    height: 42px;
    border-radius: 11px;
    background: #eaf2eb;
    color: #174d38;
    display: flex;
    align-items: center;
    justify-content: center;
}

.info-card h3 {
    font-size: 15px;
}

.info-card p {
    font-size: 11px;
    color: #7c8980;
    line-height: 1.5;
    margin-top: 5px;
}

/* =========================================================
   PLANNER
========================================================= */

.planner-container {
    padding: 60px 7%;
}

.planner-title {
    text-align: center;
    margin-bottom: 45px;
}

.planner-title h1 {
    font-size: 45px;
    line-height: 1.05;
    margin: 12px 0;
}

.planner-title h1 span {
    color: #4e8063;
}

.planner-title p {
    color: #77837b;
}

.planner-grid {
    display: grid;
    grid-template-columns: 1.4fr .8fr;
    gap: 30px;
    max-width: 1100px;
    margin: auto;
}

.planner-form {
    display: flex;
    flex-direction: column;
    gap: 17px;
}

.form-card {
    background: white;
    border: 1px solid #e4eae4;
    border-radius: 17px;
    padding: 24px;
}

.form-heading {
    display: flex;
    gap: 14px;
    align-items: center;
}

.form-heading > svg {
    color: #174d38;
}

.form-heading h3 {
    font-size: 16px;
}

.form-heading p {
    font-size: 11px;
    color: #849087;
    margin-top: 4px;
}

.day-selector {
    margin-top: 25px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 35px;
}

.day-selector button {
    width: 40px;
    height: 40px;
    border: 1px solid #dce3dc;
    background: white;
    border-radius: 10px;
}

.day-selector div {
    text-align: center;
}

.day-selector strong {
    font-size: 34px;
    display: block;
}

.day-selector span {
    color: #7d8981;
    font-size: 11px;
}

.budget-input {
    display: flex;
    align-items: center;
    border: 1px solid #dce3dc;
    border-radius: 12px;
    padding: 3px 15px;
    margin-top: 22px;
}

.budget-input span {
    font-size: 22px;
    font-weight: bold;
}

.budget-input input {
    width: 100%;
    border: none;
    outline: none;
    padding: 13px;
    font-size: 21px;
}

.budget-suggestions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 12px;
}

.budget-suggestions button {
    background: #f1f5f1;
    border: none;
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 11px;
}

.traveler-options {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 9px;
    margin-top: 20px;
}

.traveler-options button {
    border: 1px solid #dfe6df;
    background: white;
    padding: 13px 5px;
    border-radius: 10px;
    font-size: 11px;
}

.traveler-options button.selected {
    border-color: #4e8063;
    background: #edf5ef;
    color: #174d38;
}

.traveler-icon {
    display: block;
    font-size: 20px;
    margin-bottom: 6px;
}

.interest-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 20px;
}

.interest-grid button {
    background: white;
    border: 1px solid #dfe6df;
    padding: 10px;
    border-radius: 9px;
    font-size: 11px;
}

.interest-grid button.selected {
    background: #eaf3ec;
    color: #174d38;
    border-color: #5a876b;
}

.generate-button {
    justify-content: center;
    padding: 17px;
    font-size: 14px;
}

.planner-preview {
    background: white;
    border-radius: 18px;
    border: 1px solid #e4eae4;
    overflow: hidden;
    height: fit-content;
    position: sticky;
    top: 100px;
}

.planner-preview > img {
    width: 100%;
    height: 220px;
    object-fit: cover;
}

.preview-body {
    padding: 24px;
}

.preview-body h3 {
    font-size: 27px;
    margin: 8px 0;
}

.preview-body > p {
    color: #7d8981;
    font-size: 12px;
    display: flex;
    gap: 5px;
}

.preview-divider {
    border-top: 1px solid #edf0ed;
    margin: 20px 0;
}

.preview-row {
    display: flex;
    justify-content: space-between;
    margin: 15px 0;
    font-size: 12px;
}

.preview-row span {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #78847c;
}

.preview-row strong {
    color: #173f30;
}

.preview-interests {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.preview-interests span {
    background: #eef4ef;
    padding: 6px 9px;
    border-radius: 7px;
    color: #42604e;
    font-size: 10px;
}

/* =========================================================
   TRIP PAGE
========================================================= */

.trip-header {
    background: white;
    padding: 50px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e5ebe5;
}

.trip-header h1 {
    font-size: 42px;
    margin: 10px 0;
}

.trip-header h1 span {
    color: #4e8063;
}

.trip-meta {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.trip-meta span {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #6e7d73;
    font-size: 12px;
}

.ai-chat-button {
    background: #174d38;
    border: none;
    color: white;
    padding: 13px 18px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.trip-container {
    padding: 50px 7%;
    display: grid;
    grid-template-columns: 1.5fr .75fr;
    gap: 30px;
}

.itinerary {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.day-card {
    background: white;
    border: 1px solid #e4eae4;
    border-radius: 15px;
    padding: 20px;
    display: flex;
    gap: 20px;
}

.day-number {
    width: 58px;
    height: 65px;
    background: #eaf2eb;
    color: #174d38;
    border-radius: 11px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.day-number span {
    font-size: 8px;
    letter-spacing: 1px;
}

.day-number strong {
    font-size: 25px;
}

.day-content {
    flex: 1;
}

.day-title {
    display: flex;
    justify-content: space-between;
}

.day-title h3 {
    font-size: 17px;
}

.day-title p {
    font-size: 12px;
    color: #7b877f;
    margin-top: 5px;
}

.place-list {
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
    margin-top: 14px;
}

.place-list span {
    background: #f2f5f2;
    padding: 7px 9px;
    border-radius: 7px;
    font-size: 10px;
    display: flex;
    gap: 5px;
    align-items: center;
    color: #53645a;
}

.trip-sidebar {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.sidebar-card {
    background: white;
    border: 1px solid #e4eae4;
    border-radius: 15px;
    padding: 20px;
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 20px;
    color: #174d38;
}

.sidebar-title h3 {
    color: #26392e;
    font-size: 15px;
}

.total-budget {
    display: flex;
    justify-content: space-between;
    margin-bottom: 18px;
}

.total-budget span {
    color: #7b877f;
    font-size: 11px;
}

.total-budget strong {
    color: #174d38;
}

.budget-line {
    margin-top: 15px;
}

.budget-line-top {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #6d7b72;
}

.budget-line-top strong {
    color: #344b3c;
}

.progress {
    height: 5px;
    background: #edf0ed;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 7px;
}

.progress-value {
    height: 100%;
    background: #5e8b6d;
    border-radius: 10px;
}

.food-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 13px;
}

.food-icon {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: #edf4ee;
    color: #477052;
    display: flex;
    align-items: center;
    justify-content: center;
}

.food-item div:nth-child(2) {
    flex: 1;
}

.food-item strong {
    display: block;
    font-size: 11px;
}

.food-item span {
    display: block;
    color: #89938d;
    font-size: 9px;
    margin-top: 3px;
}

.packing-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    margin: 11px 0;
    color: #59675f;
}

.packing-item svg {
    color: #4e8063;
}

.dont-pack {
    background: #fff4f1;
    color: #a65e52;
    padding: 9px;
    border-radius: 8px;
    font-size: 10px;
    display: flex;
    gap: 7px;
    margin-top: 15px;
}

.weather-card {
    display: flex;
    gap: 13px;
    background: #f0f5ef;
}

.weather-card > div:first-child {
    color: #c18b2b;
}

.weather-card span,
.weather-card strong,
.weather-card p {
    display: block;
}

.weather-card span {
    font-size: 9px;
    color: #79857d;
}

.weather-card strong {
    font-size: 13px;
    margin-top: 4px;
}

.weather-card p {
    color: #7b877f;
    font-size: 9px;
    margin-top: 4px;
}

/* =========================================================
   AI CHAT
========================================================= */

.floating-ai {
    position: fixed;
    right: 25px;
    bottom: 25px;
    z-index: 50;
    background: #174d38;
    color: white;
    border: none;
    border-radius: 30px;
    padding: 13px 18px;
    display: flex;
    gap: 8px;
    align-items: center;
    box-shadow: 0 10px 30px rgba(23,77,56,.3);
}

.chat-window {
    position: fixed;
    right: 25px;
    bottom: 25px;
    width: 370px;
    height: 540px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 20px 60px rgba(20,40,30,.25);
    z-index: 100;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    border: 1px solid #dfe7df;
}

.chat-header {
    background: #174d38;
    color: white;
    padding: 17px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-header button {
    background: transparent;
    color: white;
    border: none;
}

.chat-title {
    display: flex;
    gap: 10px;
    align-items: center;
}

.ai-avatar {
    width: 35px;
    height: 35px;
    border-radius: 10px;
    background: rgba(255,255,255,.15);
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-title strong,
.chat-title span {
    display: block;
}

.chat-title strong {
    font-size: 13px;
}

.chat-title span {
    font-size: 9px;
    color: #b9d2c1;
    margin-top: 3px;
}

.chat-body {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    background: #f7f9f7;
}

.chat-message {
    max-width: 84%;
    padding: 11px 13px;
    border-radius: 13px;
    font-size: 11px;
    line-height: 1.55;
    margin-bottom: 9px;
}

.chat-message.ai {
    background: white;
    color: #46554c;
    border: 1px solid #e7ebe7;
}

.chat-message.user {
    margin-left: auto;
    background: #174d38;
    color: white;
}

.chat-suggestions {
    display: flex;
    gap: 5px;
    padding: 8px 10px;
    overflow-x: auto;
}

.chat-suggestions button {
    white-space: nowrap;
    border: 1px solid #dfe6df;
    background: white;
    padding: 6px 8px;
    border-radius: 8px;
    font-size: 9px;
}

.chat-input {
    border-top: 1px solid #e7ebe7;
    display: flex;
    padding: 9px;
}

.chat-input input {
    flex: 1;
    border: none;
    outline: none;
    padding: 10px;
    font-size: 11px;
}

.chat-input button {
    width: 38px;
    border: none;
    border-radius: 9px;
    background: #174d38;
    color: white;
}

/* =========================================================
   EMPTY
========================================================= */

.empty {
    text-align: center;
    padding: 80px 20px;
    color: #738077;
}

.empty h3 {
    color: #24382c;
    margin: 15px 0 7px;
}

/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 950px) {

    .destination-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .feature-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .planner-grid,
    .trip-container,
    .details-content {
        grid-template-columns: 1fr;
    }

    .planner-preview {
        position: static;
    }

    .trip-sidebar {
        order: -1;
    }
}

@media (max-width: 650px) {

    .navbar {
        padding: 0 5%;
    }

    .nav-links,
    .nav-right .icon-button,
    .nav-right .profile div:not(.avatar) {
        display: none;
    }

    .hero {
        padding: 55px 6%;
    }

    .hero h1 {
        font-size: 44px;
    }

    .content,
    .features-section,
    .planner-container,
    .trip-container,
    .details-content {
        padding: 45px 5%;
    }

    .destination-grid,
    .feature-grid,
    .info-cards {
        grid-template-columns: 1fr;
    }

    .section-heading {
        align-items: start;
        gap: 10px;
    }

    .destination-overlay h1 {
        font-size: 45px;
    }

    .destination-overlay {
        padding: 6%;
    }

    .traveler-options {
        grid-template-columns: repeat(2, 1fr);
    }

    .interest-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .trip-header {
        padding: 40px 5%;
        flex-direction: column;
        align-items: start;
        gap: 20px;
    }

    .trip-header h1 {
        font-size: 33px;
    }

    .chat-window {
        left: 12px;
        right: 12px;
        width: auto;
        bottom: 12px;
        height: 520px;
    }

    .floating-ai {
        right: 15px;
        bottom: 15px;
    }

    .footer {
        flex-direction: column;
        gap: 15px;
        align-items: start;
    }
}

</style>

</head>

<body>

<div id="app"></div>

<script>

const destinations = {{ destinations | tojson }};
destinations.forEach((d, index) => { d.id = index + 1; });

let selected = null;
let currentPage = "home";

let days = 5;
let budget = 100000;
let travelers = "Couple";
let interests = ["Food", "Nature"];

let saved = JSON.parse(localStorage.getItem("voyanta_saved") || "[]");
saved = Array.isArray(saved) ? saved.filter(id => destinations.some(d => d.id === id)) : [];
let userName = "Gowri";

// Each country's Voyanta AI conversation is stored separately.
// Switching countries starts a separate chat instead of mixing conversations.
let chatHistoryByCountry = JSON.parse(localStorage.getItem("voyanta_chat_history_by_country") || "{}");
if(!chatHistoryByCountry || typeof chatHistoryByCountry !== "object" || Array.isArray(chatHistoryByCountry)) {
    chatHistoryByCountry = {};
}

let chatMessages = [
    {
        from: "ai",
        text: `Hello ${userName}! 👋 I'm Voyanta AI ✨ Ask me anything about your destination, itinerary, food, budget or travel tips.`
    }
];

function chatCountryKey(country) {
    return (country || "general").trim().toLowerCase();
}

function saveChatForCountry(country) {
    const key = chatCountryKey(country);
    if(!key) return;

    // Save the complete conversation for this country.
    chatHistoryByCountry[key] = chatMessages;
    localStorage.setItem(
        "voyanta_chat_history_by_country",
        JSON.stringify(chatHistoryByCountry)
    );
}

function loadChatForCountry(country) {
    const key = chatCountryKey(country);
    const savedChat = chatHistoryByCountry[key];

    if(Array.isArray(savedChat) && savedChat.length > 0) {
        chatMessages = savedChat;
    } else {
        chatMessages = [
            {
                from: "ai",
                text: `Hello ${userName}! 👋 I'm Voyanta AI ✨ Let's plan your ${country} trip. Ask me anything about ${country}, food, places, hotels, budget, itinerary or travel tips.`
            }
        ];
    }
}

function saveCurrentChatBeforeLeaving() {
    if(selected && selected.country) {
        saveChatForCountry(selected.country);
    }
}


// ============================================================
// HOME
// ============================================================

function homePage() {

    currentPage = "home";

    document.getElementById("app").innerHTML = `

    ${navbar()}

    <section class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                ✨ AI-powered travel intelligence
            </div>

            <h1>
                Travel smarter.<br>
                <span>Experience more.</span>
            </h1>

            <p>
                Tell Voyanta where you want to go.
                We'll help you plan the perfect trip around
                your days, budget and travel style.
            </p>

            <div class="search-box">

                🔎

                <input
                    id="search"
                    placeholder="Search any destination..."
                    oninput="searchDestination()"
                >

            </div>

            <div class="quick-searches">

                <span>Popular:</span>

                <button onclick="quickSearch('Finland')">
                    Finland
                </button>

                <button onclick="quickSearch('Paris')">
                    Paris
                </button>

                <button onclick="quickSearch('Tokyo')">
                    Tokyo
                </button>

                <button onclick="quickSearch('Goa')">
                    Goa
                </button>

            </div>

        </div>

    </section>


    <main class="content">

        <div class="section-heading">

            <div>
                <span class="eyebrow">DISCOVER</span>
                <h2>Where will you go next?</h2>
            </div>

            <span class="result-count">
                ${destinations.length} destinations
            </span>

        </div>

        <div
            id="destinationGrid"
            class="destination-grid"
        >

            ${destinationCards(destinations)}

        </div>

    </main>


    <section class="features-section">

        <div class="section-heading centered">

            <span class="eyebrow">
                WHY VOYANTA
            </span>

            <h2>
                Your personal travel intelligence
            </h2>

        </div>


        <div class="feature-grid">

            ${feature(
                "✨",
                "AI Trip Planning",
                "Get a personalised day-by-day itinerary based on your preferences."
            )}

            ${feature(
                "₹",
                "Budget Aware",
                "Plan comfortably within your own budget — from ₹10,000 to ₹20 lakh+."
            )}

            ${feature(
                "🧭",
                "Travel Your Way",
                "Choose solo, couple, family or friends and customise your interests."
            )}

            ${feature(
                "💬",
                "Ask Voyanta",
                "Chat with your AI travel assistant whenever you need help."
            )}

        </div>

    </section>


    <footer class="footer">

        <div class="brand">
            <div class="brand-icon">🧭</div>
            <div class="brand-name">Voyanta</div>
        </div>

        <p>
            AI-powered travel planning for better journeys.
        </p>

        <span>
            © 2026 Voyanta
        </span>

    </footer>

    `;

}


// ============================================================
// NAVBAR
// ============================================================

function navbar() {

return `

<header class="navbar">

    <div
        class="brand"
        onclick="homePage()"
    >

        <div class="brand-icon">
            🧭
        </div>

        <div>

            <div class="brand-name">
                Voyanta
            </div>

            <div class="brand-sub">
                AI TRAVEL PLANNER
            </div>

        </div>

    </div>


    <div class="nav-links">

        <button
            class="active"
            onclick="homePage()"
        >
            Explore
        </button>

        <button onclick="savedPage()">
            Saved
        </button>

        <button onclick="tripPage()">
            My Trips
        </button>

    </div>


    <div class="nav-right">

        <button class="icon-button">
            🔔
        </button>

        <div class="profile">

            <div class="avatar">
                ${userName.charAt(0).toUpperCase()}
            </div>

            <div>

                <strong>
                    ${userName}
                </strong>

                <span>
                    Traveler
                </span>

            </div>

        </div>

    </div>

</header>

`;

}


// ============================================================
// DESTINATION CARDS
// ============================================================

function destinationCards(list) {

if(list.length === 0) {
return `
<div class="empty">
    <h3>No destination found</h3>
    <p>Try another destination or search by country, region or interest.</p>
</div>`;
}

return list.map((d) => `
<div class="destination-card" onclick="openDestinationById(${d.id})">
    <div class="destination-image">
        <img src="${d.image}" alt="${d.name}">
        <button
            type="button"
            class="save-button ${saved.includes(d.id) ? "saved" : ""}"
            aria-label="${saved.includes(d.id) ? "Unsave" : "Save"} ${d.name}"
            onclick="event.preventDefault(); event.stopPropagation(); toggleSave(${d.id}, this); return false;"
        >
            ${saved.includes(d.id) ? "♥" : "♡"}
        </button>
        <div class="image-region">${d.region}</div>
    </div>
    <div class="destination-info">
        <div class="destination-title-row">
            <div>
                <h3>${d.name}</h3>
                <p>📍 ${d.country}</p>
            </div>
            <div class="rating">★ ${d.rating}</div>
        </div>
        <p class="destination-description">${d.description}</p>
        <div class="tag-row">
            ${d.tags.map(tag => `<span>${tag}</span>`).join("")}
        </div>
        <div class="card-footer">
            <span>From <strong>${d.price}</strong></span>
            <span>Plan →</span>
        </div>
    </div>
</div>
`).join("");
}


// ============================================================
// FEATURE
// ============================================================

function feature(icon, title, text) {

return `

<div class="feature-card">

    <div class="feature-icon">
        ${icon}
    </div>

    <h3>
        ${title}
    </h3>

    <p>
        ${text}
    </p>

</div>

`;

}


// ============================================================
// SEARCH
// ============================================================

function searchDestination() {

const value =
    document.getElementById("search").value.toLowerCase();

const result =
    destinations.filter(d =>
        d.name.toLowerCase().includes(value) ||
        d.country.toLowerCase().includes(value) ||
        d.region.toLowerCase().includes(value) ||
        d.tags.some(
            tag => tag.toLowerCase().includes(value)
        )
    );

document.getElementById("destinationGrid").innerHTML =
    destinationCards(result);

}


function quickSearch(name) {

document.getElementById("search").value = name;

searchDestination();

window.scrollTo({
    top: 550,
    behavior: "smooth"
});

}


// ============================================================
// SAVE
// ============================================================

function toggleSave(id, button) {

if(saved.includes(id)) {
    saved = saved.filter(x => x !== id);
    if(button) {
        button.textContent = "♡";
        button.classList.remove("saved");
        button.setAttribute("aria-label", "Save " + (destinations.find(d => d.id === id)?.name || "destination"));
    }
} else {
    saved.push(id);
    if(button) {
        button.textContent = "♥";
        button.classList.add("saved");
        button.setAttribute("aria-label", "Unsave " + (destinations.find(d => d.id === id)?.name || "destination"));
    }
}

localStorage.setItem("voyanta_saved", JSON.stringify(saved));

}


// ============================================================
// DESTINATION PAGE
// ============================================================

function resetChatForNewCountry(country) {

    // IMPORTANT: save the old country's conversation before leaving it.
    // The new country gets its own independent conversation.
    loadChatForCountry(country);

    // If the chat is currently open while changing country, close it so the
    // old country's messages can never remain visible in the new country.
    const oldChat = document.getElementById("chatWindow");
    if(oldChat) oldChat.remove();
}


function openDestinationById(id) {

    const nextDestination = destinations.find(d => d.id === id);
    if(!nextDestination) return;

    const previousCountry = selected ? selected.country : "";

    // Save the conversation belonging to the country we are leaving.
    if(previousCountry && previousCountry !== nextDestination.country) {
        saveChatForCountry(previousCountry);
    }

    selected = nextDestination;

    // Every country has a separate chat. If this country was used before,
    // restore its saved conversation; otherwise start a brand-new chat.
    if(previousCountry !== selected.country) {
        resetChatForNewCountry(selected.country);
    }

    plannerPage();
}


function destinationPage() {

currentPage = "destination";

document.getElementById("app").innerHTML = `

${navbar()}

<div class="page-header">

    <button
        class="back-button"
        onclick="homePage()"
    >
        ← Back
    </button>

</div>


<section class="destination-hero">

    <img
        src="${selected.image}"
        alt="${selected.name}"
    >

    <div class="destination-overlay">

        <div>

            <span class="hero-location">
                📍 ${selected.country}
            </span>

            <h1>
                ${selected.name}
            </h1>

            <p>
                ${selected.description}
            </p>

            <div class="hero-rating">
                ★ ${selected.rating} Excellent
            </div>

        </div>

    </div>

</section>


<section class="details-content">

    <div class="details-main">

        <span class="eyebrow">
            EXPLORE ${selected.name.toUpperCase()}
        </span>

        <h2>
            Ready to plan your trip?
        </h2>

        <p class="large-text">

            Tell Voyanta how long you're staying
            and your budget. We'll build a personalised
            experience for you.

        </p>


        <div class="interest-preview">

            ${selected.tags.map(
                x => `<span>✓ ${x}</span>`
            ).join("")}

        </div>


        <button
            class="primary-button large"
            onclick="plannerPage()"
        >
            ✨ Plan my trip →
        </button>

    </div>


    <div class="info-cards">

        ${infoCard(
            "🏨",
            "Stay",
            "Hotels, resorts and stays based on your budget."
        )}

        ${infoCard(
            "🍴",
            "Food",
            "Local dishes and restaurant recommendations."
        )}

        ${infoCard(
            "📷",
            "Places",
            "Top attractions, hidden gems and photo spots."
        )}

        ${infoCard(
            "🧭",
            "Activities",
            "Fun experiences based on your travel style."
        )}

    </div>

</section>

`;

}


// ============================================================
// INFO CARD
// ============================================================

function infoCard(icon, title, text) {

return `

<div class="info-card">

    <div class="info-icon">
        ${icon}
    </div>

    <div>

        <h3>
            ${title}
        </h3>

        <p>
            ${text}
        </p>

    </div>

</div>

`;

}


// ============================================================
// PLANNER
// ============================================================

function plannerPage() {

document.getElementById("app").innerHTML = `

${navbar()}

<main class="planner-container">

    <div class="planner-title">

        <span class="eyebrow">
            PLAN YOUR JOURNEY
        </span>

        <h1>
            Let's design your<br>
            <span>${selected.name} trip.</span>
        </h1>

        <p>
            A few details are all we need to create
            your personalised travel plan.
        </p>

    </div>


    <div class="planner-grid">

        <div class="planner-form">

            <!-- DAYS -->

            <div class="form-card">

                <div class="form-heading">

                    📅

                    <div>

                        <h3>
                            How long are you staying?
                        </h3>

                        <p>
                            Choose the number of days.
                        </p>

                    </div>

                </div>


                <div class="day-selector">

                    <button onclick="changeDays(-1)">
                        −
                    </button>

                    <div>

                        <strong id="daysValue">
                            ${days}
                        </strong>

                        <span>
                            Days
                        </span>

                    </div>

                    <button onclick="changeDays(1)">
                        +
                    </button>

                </div>

            </div>


            <!-- BUDGET -->

            <div class="form-card">

                <div class="form-heading">

                    ₹

                    <div>

                        <h3>
                            What's your budget?
                        </h3>

                        <p>
                            Enter any amount in Indian Rupees.
                        </p>

                    </div>

                </div>


                <div class="budget-input">

                    <span>₹</span>

                    <input
                        id="budgetInput"
                        type="number"
                        value="${budget}"
                        onchange="updateBudget()"
                    >

                </div>


                <div class="budget-suggestions">

                    <button onclick="setBudget(25000)">
                        ₹25K
                    </button>

                    <button onclick="setBudget(50000)">
                        ₹50K
                    </button>

                    <button onclick="setBudget(100000)">
                        ₹1L
                    </button>

                    <button onclick="setBudget(500000)">
                        ₹5L
                    </button>

                    <button onclick="setBudget(2000000)">
                        ₹20L
                    </button>

                </div>

            </div>


            <!-- TRAVELERS -->

            <div class="form-card">

                <div class="form-heading">

                    👥

                    <div>

                        <h3>
                            Who's travelling?
                        </h3>

                        <p>
                            Choose your travel style.
                        </p>

                    </div>

                </div>


                <div class="traveler-options">

                    ${travelerButton("Solo", "🧍")}
                    ${travelerButton("Couple", "👫")}
                    ${travelerButton("Family", "👨‍👩‍👧")}
                    ${travelerButton("Friends", "👯")}

                </div>

            </div>


            <!-- INTERESTS -->

            <div class="form-card">

                <div class="form-heading">

                    ✨

                    <div>

                        <h3>
                            What do you enjoy?
                        </h3>

                        <p>
                            Select as many interests as you want.
                        </p>

                    </div>

                </div>


                <div class="interest-grid">

                    ${[
                        "Food",
                        "Nature",
                        "Adventure",
                        "Culture",
                        "Shopping",
                        "Nightlife",
                        "Photography",
                        "Relaxation"
                    ].map(x => `

                        <button
                            class="${interests.includes(x) ? "selected" : ""}"
                            onclick="toggleInterest('${x}')"
                        >
                            ${x}
                        </button>

                    `).join("")}

                </div>

            </div>


            <button
                class="primary-button generate-button"
                onclick="generateTrip()"
            >
                ✨ Generate my trip →
            </button>

        </div>


        <!-- PREVIEW -->

        <aside class="planner-preview">

            <img
                src="${selected.image}"
            >

            <div class="preview-body">

                <span class="eyebrow">
                    YOUR DESTINATION
                </span>

                <h3>
                    ${selected.name}
                </h3>

                <p>
                    📍 ${selected.country}
                </p>

                <div class="preview-divider"></div>


                <div class="preview-row">

                    <span>
                        📅 Duration
                    </span>

                    <strong>
                        ${days} days
                    </strong>

                </div>


                <div class="preview-row">

                    <span>
                        ₹ Budget
                    </span>

                    <strong>
                        ₹${budget.toLocaleString("en-IN")}
                    </strong>

                </div>


                <div class="preview-row">

                    <span>
                        👥 Travelling
                    </span>

                    <strong>
                        ${travelers}
                    </strong>

                </div>


                <div class="preview-divider"></div>


                <div class="preview-interests">

                    ${interests.map(
                        x => `<span>${x}</span>`
                    ).join("")}

                </div>

            </div>

        </aside>

    </div>

</main>

`;

}


function travelerButton(name, icon) {

return `

<button
    class="${travelers === name ? "selected" : ""}"
    onclick="selectTraveler('${name}')"
>

    <span class="traveler-icon">
        ${icon}
    </span>

    ${name}

</button>

`;

}


function selectTraveler(name) {

travelers = name;

plannerPage();

}


function changeDays(value) {

days = Math.max(1, days + value);

plannerPage();

}


function setBudget(value) {

budget = value;

plannerPage();

}


function updateBudget() {

const value =
    Number(document.getElementById("budgetInput").value);

if(value >= 0) {
    budget = value;
}

}


function toggleInterest(item) {

if(interests.includes(item)) {

interests =
    interests.filter(x => x !== item);

} else {

interests.push(item);

}

plannerPage();

}


// ============================================================
// GENERATE TRIP
// ============================================================

function generateTrip() {

tripPage();

}


// ============================================================
// TRIP PAGE
// ============================================================

function tripPage() {

if(!selected) {

homePage();

return;

}


let accommodation = Math.round(budget * .35);
let food = Math.round(budget * .20);
let transport = Math.round(budget * .15);
let activities = Math.round(budget * .20);
let shopping = Math.round(budget * .10);


let itinerary = "";

const activitiesList = [

[
"Arrival & Local Exploration",
"Check in, relax and explore the nearby area.",
["Hotel Check-in", "Local Market", "Evening Walk"]
],

[
"Main Attractions",
"Visit the most famous landmarks and must-see attractions.",
["Top Landmark", "City Centre", "Photo Spot"]
],

[
"Food & Culture",
"Experience local cuisine, markets and cultural activities.",
["Local Restaurant", "Cultural Area", "Food Street"]
],

[
"Adventure Day",
"Try exciting activities and explore scenic locations.",
["Adventure Activity", "Scenic View", "Sunset Point"]
],

[
"Relax & Shopping",
"Enjoy a relaxed morning and shop for local souvenirs.",
["Shopping District", "Café", "Local Attraction"]
]

];


for(let i = 0; i < days; i++) {

let a =
    activitiesList[i % activitiesList.length];

itinerary += `

<div class="day-card">

    <div class="day-number">

        <span>DAY</span>

        <strong>
            ${i + 1}
        </strong>

    </div>


    <div class="day-content">

        <div class="day-title">

            <div>

                <h3>
                    ${a[0]}
                </h3>

                <p>
                    ${a[1]}
                </p>

            </div>

            <span>
                🕐
            </span>

        </div>


        <div class="place-list">

            ${a[2].map(
                x => `<span>📍 ${x}</span>`
            ).join("")}

        </div>

    </div>

</div>

`;

}


document.getElementById("app").innerHTML = `

${navbar()}

<section class="trip-header">

    <div>

        <span class="eyebrow">
            YOUR AI-GENERATED TRIP
        </span>

        <h1>
            ${days} days in
            <span>${selected.name}</span>
        </h1>


        <div class="trip-meta">

            <span>
                📅 ${days} days
            </span>

            <span>
                ₹ ${budget.toLocaleString("en-IN")}
            </span>

            <span>
                👥 ${travelers}
            </span>

        </div>

    </div>


    <button
        class="ai-chat-button"
        onclick="openChat()"
    >
        💬 Ask Voyanta AI
    </button>

</section>


<main class="trip-container">

    <section>

        <div class="section-heading">

            <div>

                <span class="eyebrow">
                    DAY BY DAY
                </span>

                <h2>
                    Your itinerary
                </h2>

            </div>

        </div>


        <div class="itinerary">

            ${itinerary}

        </div>

    </section>


    <aside class="trip-sidebar">

        <!-- BUDGET -->

        <div class="sidebar-card">

            <div class="sidebar-title">

                💰

                <h3>
                    Budget breakdown
                </h3>

            </div>


            <div class="total-budget">

                <span>
                    Total budget
                </span>

                <strong>
                    ₹${budget.toLocaleString("en-IN")}
                </strong>

            </div>


            ${budgetLine(
                "Accommodation",
                accommodation,
                budget
            )}

            ${budgetLine(
                "Food",
                food,
                budget
            )}

            ${budgetLine(
                "Transport",
                transport,
                budget
            )}

            ${budgetLine(
                "Activities",
                activities,
                budget
            )}

            ${budgetLine(
                "Shopping",
                shopping,
                budget
            )}

        </div>


        <!-- FOOD -->

        <div class="sidebar-card">

            <div class="sidebar-title">

                🍴

                <h3>
                    Food to try
                </h3>

            </div>


            ${foodItem(
                "Local Speciality",
                "Authentic local cuisine"
            )}

            ${foodItem(
                "Street Food",
                "Popular local flavours"
            )}

            ${foodItem(
                "Signature Dessert",
                "A must-try sweet treat"
            )}

        </div>


        <!-- PACKING -->

        <div class="sidebar-card">

            <div class="sidebar-title">

                🎒

                <h3>
                    Smart packing list
                </h3>

            </div>


            ${[
                "Travel documents",
                "Comfortable shoes",
                "Weather-appropriate clothes",
                "Phone charger & power bank",
                "Toiletries"
            ].map(
                x => `<div class="packing-item">✓ ${x}</div>`
            ).join("")}


            <div class="dont-pack">
                ✕ Avoid unnecessary heavy luggage
            </div>

        </div>


        <div class="sidebar-card weather-card">

            ☀️

            <div>

                <span>
                    Typical experience
                </span>

                <strong>
                    Check local weather
                </strong>

                <p>
                    Pack according to the current season.
                </p>

            </div>

        </div>

    </aside>

</main>

`;

}


function budgetLine(label, value, total) {

let percent =
    total ? Math.round(value / total * 100) : 0;

return `

<div class="budget-line">

    <div class="budget-line-top">

        <span>
            ${label}
        </span>

        <strong>
            ₹${value.toLocaleString("en-IN")}
        </strong>

    </div>


    <div class="progress">

        <div
            class="progress-value"
            style="width:${percent}%"
        ></div>

    </div>

</div>

`;

}


function foodItem(name, text) {

return `

<div class="food-item">

    <div class="food-icon">
        🍴
    </div>

    <div>

        <strong>
            ${name}
        </strong>

        <span>
            ${text}
        </span>

    </div>

    →

</div>

`;

}


// ============================================================
// SAVED PAGE
// ============================================================

function savedPage() {

const items =
    destinations.filter(
        d => saved.includes(d.id)
    );


document.getElementById("app").innerHTML = `

${navbar()}

<main class="content">

    <div class="section-heading">

        <div>

            <span class="eyebrow">
                YOUR COLLECTION
            </span>

            <h2>
                Saved destinations
            </h2>

        </div>

    </div>


    ${
        items.length === 0
        ?
        `
        <div class="empty">

            <h3>
                ♡ No saved destinations
            </h3>

            <p>
                Tap the heart icon on a destination to save it here.
            </p>

        </div>
        `
        :
        `
        <div class="destination-grid">

            ${destinationCards(items)}

        </div>
        `
    }

</main>

`;

}


// ============================================================
// AI CHAT
// ============================================================

function openChat() {

if(document.getElementById("chatWindow")) {

document.getElementById("chatWindow").remove();

return;

}


document.body.insertAdjacentHTML(
"beforeend",
chatHTML()
);

renderChat();

}


function chatHTML() {

return `

<div
    id="chatWindow"
    class="chat-window"
>

    <div class="chat-header">

        <div class="chat-title">

            <div class="ai-avatar">
                ✨
            </div>

            <div>

                <strong>
                    Voyanta AI
                </strong>

                <span>
                    Travel assistant
                </span>

            </div>

        </div>


        <button onclick="closeChat()">
            ✕
        </button>

    </div>


    <div
        id="chatBody"
        class="chat-body"
    ></div>


    <div class="chat-suggestions">

        <button
            onclick="quickMessage('What food should I try?')"
        >
            Food recommendations
        </button>

        <button
            onclick="quickMessage('Help me with packing')"
        >
            Packing
        </button>

        <button
            onclick="quickMessage('Is my budget enough?')"
        >
            Budget
        </button>

    </div>


    <div class="chat-input">

        <input
            id="chatInput"
            placeholder="Ask anything..."
            onkeydown="if(event.key==='Enter') sendChat()"
        >

        <button onclick="sendChat()">
            ➤
        </button>

    </div>

</div>

`;

}


function closeChat() {

const chat =
    document.getElementById("chatWindow");

if(chat) chat.remove();

}


function renderChat() {

const body =
    document.getElementById("chatBody");

if(!body) return;

body.innerHTML =
    chatMessages.map(
        m => `
        <div class="chat-message ${m.from}">
            ${m.text}
        </div>
        `
    ).join("");

body.scrollTop = body.scrollHeight;

}


function quickMessage(text) {

document.getElementById("chatInput").value = text;

sendChat();

}


async function sendChat() {

const input = document.getElementById("chatInput");
if(!input) return;

const text = input.value.trim();
if(!text) return;

chatMessages.push({ from: "user", text: text });
input.value = "";
renderChat();

try {
    const result = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: text,
            // Send the current country conversation too, so follow-up questions such as
            // "what about the weather?" or "tell me more" keep their meaning.
            history: chatMessages.slice(-16),
            destination: selected ? selected.name : "",
            country: selected ? selected.country : "",
            travelers: travelers,
            days: days,
            budget: budget,
            interests: interests
        })
    });

    const data = await result.json();
    const response = data.answer || "Sorry, I couldn't answer that right now.";

    chatMessages.push({ from: "ai", text: response });
    saveChatForCountry(selected ? selected.country : "general");
    renderChat();
} catch (error) {
    chatMessages.push({
        from: "ai",
        text: "Sorry, Voyanta AI is temporarily unavailable. Please try again."
    });
    saveChatForCountry(selected ? selected.country : "general");
    renderChat();
}

}


// ============================================================
// START
// ============================================================

homePage();

</script>

</body>
</html>
"""


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template_string(
        HTML,
        destinations=DESTINATIONS
    )


@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"answer": "Please ask me a question."}), 400

    destination = str(data.get("destination", "")).strip() or "not selected"
    country = str(data.get("country", "")).strip() or "unknown"
    travelers = str(data.get("travelers", "Couple"))
    days = data.get("days", 5)
    budget = data.get("budget", 100000)
    interests = data.get("interests", [])
    history = data.get("history", [])
    if not isinstance(history, list):
        history = []

    # Keep only short, useful conversation context. This makes follow-up questions
    # work naturally without changing the country-wise chat history feature.
    clean_history = []
    for item in history[-16:]:
        if isinstance(item, dict):
            role = "User" if item.get("from") == "user" else "Voyanta AI"
            text = str(item.get("text", "")).strip()
            if text:
                clean_history.append(f"{role}: {text[:1200]}")
    conversation_context = "\n".join(clean_history) or "No previous messages."

    # Country-specific knowledge used when the API is unavailable, and as grounding
    # context for the AI so different places do not receive the same generic answer.
    COUNTRY_PROFILES = {
        "Finland": {"food": "salmon soup, Finnish meatballs, rye bread and cinnamon buns", "places": "Helsinki, Rovaniemi, Lapland and the Finnish lake region", "vibe": "saunas, forests, lakes and Northern Lights", "pack": "warm layers, waterproof shoes and thermal wear in cold months"},
        "France": {"food": "croissants, crêpes, baguettes, cheese and regional French cuisine", "places": "Eiffel Tower, Louvre, Montmartre and the Seine in Paris", "vibe": "art, cafés, architecture and romantic city walks", "pack": "comfortable walking shoes and a light layer for changing weather"},
        "Japan": {"food": "sushi, ramen, tempura, okonomiyaki and matcha sweets", "places": "Tokyo, Kyoto, Osaka, Mount Fuji and traditional temples", "vibe": "food, technology, temples, anime culture and seasonal scenery", "pack": "comfortable walking shoes, light layers and an umbrella"},
        "India": {"food": "regional thalis, dosa, biryani, street food and local sweets", "places": "heritage sites, beaches, hill stations, markets and local cultural attractions", "vibe": "huge regional variety, culture, food and nature", "pack": "breathable clothes, comfortable footwear, sunscreen and a refillable water bottle"},
        "UAE": {"food": "shawarma, machboos, Arabic grills, hummus and luqaimat", "places": "Burj Khalifa, Dubai Marina, Old Dubai and desert areas", "vibe": "modern architecture, shopping, luxury and desert experiences", "pack": "light breathable clothes, sunglasses and strong sun protection"},
        "Indonesia": {"food": "nasi goreng, satay, babi guling in Bali and local tropical dishes", "places": "Ubud, Seminyak, Uluwatu, rice terraces and waterfalls", "vibe": "beaches, temples, wellness, rice terraces and nightlife", "pack": "light clothes, sandals, rain protection and modest clothing for temples"},
        "Switzerland": {"food": "fondue, raclette, rösti and Swiss chocolate", "places": "Zermatt, Interlaken, Lucerne, Jungfrau and scenic mountain railways", "vibe": "Alps, lakes, hiking and scenic train journeys", "pack": "layers, a waterproof jacket and good hiking shoes"},
        "Singapore": {"food": "chicken rice, laksa, chili crab, satay and hawker-centre dishes", "places": "Marina Bay, Gardens by the Bay, Sentosa and Chinatown", "vibe": "clean city life, hawker food, shopping and futuristic attractions", "pack": "light clothes, comfortable shoes and rain protection"},
        "Maldives": {"food": "Mas huni, fish curry, grilled seafood and coconut-based dishes", "places": "Malé, resort islands, lagoons and coral reefs", "vibe": "beaches, snorkeling, diving and relaxing island stays", "pack": "swimwear, reef-friendly sunscreen, sandals and sun protection"},
        "South Korea": {"food": "Korean barbecue, bibimbap, tteokbokki, kimchi and Korean fried chicken", "places": "Seoul palaces, Bukchon Hanok Village, N Seoul Tower and Hongdae", "vibe": "K-pop, cafés, shopping, food and historic palaces", "pack": "comfortable walking shoes and layers according to season"},
        "Hong Kong": {"food": "dim sum, roast goose, wonton noodles, egg tarts and milk tea", "places": "Victoria Peak, Tsim Sha Tsui, Central and Temple Street", "vibe": "harbour views, food, shopping and dense city energy", "pack": "comfortable shoes, light layers and rain protection"},
        "Azerbaijan": {"food": "plov, dolma, kebabs, qutab and Azerbaijani tea", "places": "Baku Old City, Flame Towers, Gobustan and the Caspian waterfront", "vibe": "Caspian city life, old architecture and Caucasus landscapes", "pack": "comfortable shoes and layers for windy or changing weather"},
        "Georgia": {"food": "khachapuri, khinkali, lobio and Georgian wine", "places": "Tbilisi Old Town, Narikala, sulfur baths and nearby mountain regions", "vibe": "historic streets, mountain scenery, food and warm hospitality", "pack": "walking shoes and layers, especially for mountain trips"},
        "Czech Republic": {"food": "goulash, svíčková, trdelník and Czech beer", "places": "Prague Old Town, Charles Bridge, Prague Castle and Petrin Hill", "vibe": "fairytale architecture, history, cafés and nightlife", "pack": "comfortable shoes and layers"},
        "Austria": {"food": "Wiener schnitzel, sachertorte, apple strudel and Austrian coffee", "places": "Vienna historic centre, Schönbrunn Palace, Belvedere and Salzburg", "vibe": "imperial architecture, classical music, cafés and Alpine scenery", "pack": "walking shoes and layers"},
        "Portugal": {"food": "pastéis de nata, bacalhau, grilled sardines and bifana", "places": "Lisbon old town, Belém, Sintra and viewpoints over the Tagus", "vibe": "coastal scenery, tiled streets, cafés and relaxed city life", "pack": "comfortable shoes, sun protection and a light jacket"},
        "Iceland": {"food": "Icelandic lamb, seafood, skyr and rye bread", "places": "Reykjavík, Golden Circle, Blue Lagoon and South Coast waterfalls", "vibe": "volcanoes, glaciers, waterfalls, geothermal pools and Northern Lights", "pack": "waterproof outerwear, warm layers and sturdy shoes"},
        "Denmark": {"food": "smørrebrød, Danish pastries, hot dogs and seafood", "places": "Copenhagen Nyhavn, Tivoli, Rosenborg and cycling districts", "vibe": "design, cycling, cafés and relaxed Nordic city life", "pack": "layers, rain protection and comfortable walking shoes"},
        "Greece": {"food": "moussaka, souvlaki, Greek salad, seafood and baklava", "places": "Athens Acropolis, Plaka, Santorini and Greek islands", "vibe": "ancient history, islands, beaches and Mediterranean food", "pack": "light clothes, sun protection and comfortable walking shoes"},
        "Canada": {"food": "poutine, maple treats, salmon and diverse multicultural cuisine", "places": "Vancouver waterfront, Stanley Park, Whistler and nearby mountains", "vibe": "mountains, lakes, outdoor activities and multicultural cities", "pack": "layers and weatherproof shoes; conditions vary by season"},
        "USA": {"food": "regional American dishes plus strong local food scenes", "places": "major city landmarks, national parks, beaches and neighbourhoods", "vibe": "varies greatly by city, from urban culture to beaches and nature", "pack": "comfortable shoes and city/season-appropriate layers"},
        "Mexico": {"food": "tacos, mole, tamales, pozole and Mexican street food", "places": "Mexico City historic centre, Chapultepec, museums and neighbourhood markets", "vibe": "food, history, art, markets and lively neighbourhoods", "pack": "comfortable shoes, sun protection and light layers"},
        "Seychelles": {"food": "Creole seafood, grilled fish, octopus curry and coconut dishes", "places": "Mahé, Praslin, La Digue and Anse Source d'Argent", "vibe": "granite beaches, snorkeling, island hopping and tropical nature", "pack": "swimwear, reef-safe sunscreen, sandals and light rainwear"},
        "Tanzania": {"food": "Zanzibari biryani, seafood, pilau, urojo and tropical fruit", "places": "Stone Town, Nungwi, Kendwa and spice-farm areas", "vibe": "beaches, Swahili culture, spices and island sunsets", "pack": "light clothes, sun protection and modest clothing for cultural sites"},
        "Mauritius": {"food": "dholl puri, seafood, rougaille and Creole dishes", "places": "Grand Baie, Le Morne, Black River Gorges and coastal lagoons", "vibe": "beaches, lagoons, hiking and multicultural food", "pack": "light clothes, swimwear, sun protection and walking shoes"},
        "Argentina": {"food": "asado, empanadas, provoleta and dulce de leche", "places": "Buenos Aires, Recoleta, Palermo and nearby cultural districts", "vibe": "steak, tango, architecture, nightlife and European-influenced culture", "pack": "comfortable shoes and layers; seasons are opposite to the Northern Hemisphere"},
        "New Zealand": {"food": "lamb, seafood, meat pies and Māori-inspired dishes", "places": "Auckland, Rotorua, Queenstown and scenic natural areas", "vibe": "adventure, mountains, lakes, Māori culture and road trips", "pack": "layers, waterproof outerwear and good outdoor shoes"},
        "United Kingdom": {"food": "fish and chips, Sunday roast, pies and afternoon tea", "places": "London landmarks, museums, Westminster, Camden and the Thames", "vibe": "history, museums, theatre, pubs and diverse city neighbourhoods", "pack": "layers, comfortable shoes and rain protection"},
        "Italy": {"food": "pizza, pasta, gelato, risotto and regional Italian dishes", "places": "Rome Colosseum, Vatican City, Trevi Fountain and historic piazzas", "vibe": "art, history, food, architecture and lively street life", "pack": "comfortable walking shoes and modest clothing for some churches"},
        "Spain": {"food": "tapas, paella, churros, jamón and regional Spanish cuisine", "places": "Barcelona Gothic Quarter, Sagrada Família, Park Güell and beaches", "vibe": "architecture, beaches, tapas, nightlife and art", "pack": "light clothes, sun protection and comfortable shoes"},
        "Netherlands": {"food": "stroopwafels, bitterballen, Dutch pancakes and herring", "places": "Amsterdam canals, Rijksmuseum, Jordaan and Vondelpark", "vibe": "canals, cycling, museums and relaxed cafés", "pack": "comfortable shoes and rain protection"},
        "Turkey": {"food": "kebabs, baklava, meze, gözleme and Turkish breakfast", "places": "Istanbul Hagia Sophia area, Blue Mosque, Grand Bazaar and Bosphorus", "vibe": "history, bazaars, mosques, Bosphorus views and rich food culture", "pack": "comfortable shoes and modest clothing for religious sites"},
        "Egypt": {"food": "koshari, ful medames, falafel and Egyptian grilled dishes", "places": "Giza Pyramids, Egyptian Museum, Khan el-Khalili and Nile areas", "vibe": "ancient history, archaeology, markets and Nile experiences", "pack": "light breathable clothes, sun protection and comfortable shoes"},
        "South Africa": {"food": "braai, bobotie, seafood and Cape Malay cuisine", "places": "Table Mountain, V&A Waterfront, Cape Point and nearby wine regions", "vibe": "mountains, coast, food, wildlife and scenic drives", "pack": "layers, sun protection and comfortable outdoor shoes"},
        "Australia": {"food": "meat pies, seafood, flat whites and multicultural Australian cuisine", "places": "Sydney Opera House, Harbour Bridge, Bondi and coastal walks", "vibe": "harbour views, beaches, cafés and outdoor city life", "pack": "sun protection, comfortable shoes and light layers"},
        "Thailand": {"food": "pad thai, tom yum, green curry, mango sticky rice and street food", "places": "Bangkok temples, markets, river areas and nearby islands", "vibe": "street food, temples, beaches, nightlife and shopping", "pack": "light breathable clothes, rain protection and modest temple clothing"},
        "Malaysia": {"food": "nasi lemak, char kway teow, laksa and satay", "places": "Petronas Twin Towers, Bukit Bintang, Batu Caves and KL food streets", "vibe": "multicultural food, shopping, city skylines and nearby nature", "pack": "light clothes, comfortable shoes and rain protection"},
        "Nepal": {"food": "dal bhat, momos, thukpa and Newari dishes", "places": "Kathmandu Durbar Square, Swayambhunath, Boudhanath and Himalayan viewpoints", "vibe": "mountains, temples, trekking and Himalayan culture", "pack": "layers, sturdy shoes and sun protection; add warm gear for high altitude"},
    }

    # Detect an explicit destination/country in the current question. This overrides
    # the selected card, so "restaurants in Japan" is answered for Japan even if Goa
    # is currently selected.
    destination_country_pairs = [(str(d.get("name", "")), str(d.get("country", ""))) for d in DESTINATIONS]
    explicit_destination = ""
    explicit_country = ""
    lower = message.lower()
    for d_name, d_country in sorted(destination_country_pairs, key=lambda x: len(x[0]), reverse=True):
        if d_name and d_name.lower() in lower:
            explicit_destination = d_name
            explicit_country = d_country
            break
    if not explicit_country:
        for c in sorted(COUNTRY_PROFILES.keys(), key=len, reverse=True):
            if c.lower() in lower:
                explicit_country = c
                break

    effective_destination = explicit_destination or destination
    effective_country = explicit_country or country
    profile = COUNTRY_PROFILES.get(effective_country, {})

    # Add exact selected-destination metadata when available.
    destination_data = next(
        (d for d in DESTINATIONS if str(d.get("name", "")).lower() == effective_destination.lower()),
        None
    )
    if destination_data is None and effective_country:
        destination_data = next(
            (d for d in DESTINATIONS if str(d.get("country", "")).lower() == effective_country.lower()),
            None
        )

    destination_details = ""
    if destination_data:
        destination_details = (
            f"name={destination_data.get('name')}; country={destination_data.get('country')}; "
            f"region={destination_data.get('region')}; description={destination_data.get('description')}; "
            f"tags={destination_data.get('tags')}; typical_budget_label={destination_data.get('price')}"
        )

    profile_text = ""
    if profile:
        profile_text = (
            f"food={profile['food']}; places={profile['places']}; "
            f"vibe={profile['vibe']}; packing={profile['pack']}"
        )

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        prompt = f"""You are Voyanta AI, the intelligent travel assistant inside a travel-planning website.

Your job is to answer the user's question itself — not just a fixed set of travel categories. The user may ask ANYTHING related to the selected place/country: food, restaurants, hotels, weather, climate, best time, visa basics, currency, language, culture, customs, safety, transport, local areas, shopping, nightlife, activities, attractions, costs, distances, family/couple/solo suitability, accessibility, itinerary, packing, or a follow-up question based on the previous chat. If the question is general but clearly connected to the place, answer it in that place's context.

IMPORTANT RULES:
1. Answer the exact question directly. Do not reply with a generic "I can help with food, places..." message.
2. Use the explicit country or destination named in the user's latest message when one is present. It overrides the currently selected destination.
3. If the user uses a follow-up such as "what about the weather?", "how much?", "is it safe?", "tell me more", or "what else?", use the conversation history to understand what "it" or "there" refers to.
4. Give location-specific details. Do not give the same answer for every country.
5. Reply in the same language/style as the user: English, Tamil, Tanglish, or mixed language.
6. Be practical and specific. Use lists when that makes the answer clearer.
7. For current information (today's weather, current restaurant hours, current prices, recent events, live availability, visa rules that may have changed), do not pretend the data is live unless verified. Say that it needs current verification.
8. Never invent a restaurant, hotel, price, opening time, visa rule, or other precise current fact.
9. If the question is outside travel, answer it normally instead of forcing it into travel context.

CURRENT SELECTED TRIP:
Destination: {destination}
Country: {country}
Traveler type: {travelers}
Days: {days}
Budget: ₹{budget}
Interests: {interests}

TARGET DETECTED FROM LATEST QUESTION:
Destination: {effective_destination}
Country: {effective_country}
Destination data: {destination_details or 'not in the built-in destination list'}
Country knowledge: {profile_text or 'Use your general knowledge for this location.'}

RECENT CONVERSATION FOR THIS COUNTRY:
{conversation_context}

LATEST USER QUESTION:
{message}

Now answer the latest question directly and naturally."""

        payload = {
            "model": "gpt-5.6-luna",
            "input": [
                {
                    "role": "system",
                    "content": "You are Voyanta AI. Answer any relevant question naturally, accurately and specifically for the user's destination. Preserve conversation context and use the user's language/style."
                },
                {"role": "user", "content": prompt}
            ],
            "max_output_tokens": 900
        }

        try:
            req = urllib.request.Request(
                "https://api.openai.com/v1/responses",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + api_key
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))

            answer = result.get("output_text", "").strip()
            if not answer:
                for item in result.get("output", []):
                    for content in item.get("content", []):
                        if content.get("type") == "output_text":
                            answer += content.get("text", "")
                answer = answer.strip()

            if answer:
                return jsonify({"answer": answer})
        except Exception:
            pass

    # Local fallback: still keep answers location-specific when the API key is not
    # available. Full natural-language answers to arbitrary questions require the AI API.
    destination_text = effective_destination if effective_destination != "not selected" else "your destination"
    country_text = effective_country if effective_country != "unknown" else "your destination country"

    if any(x in lower for x in ["hello", "hi", "hey", "vanakkam", "வணக்கம்"]):
        answer = f"Hello! 👋 I'm Voyanta AI. Ask me anything about {destination_text} in {country_text}."
    elif any(x in lower for x in ["weather", "climate", "temperature", "season", "best time", "when to go"]):
        answer = f"For {destination_text} in {country_text}, the best time and weather depend on the season. I can give a detailed answer when the AI service is connected; for current weather or forecasts, live verification is needed."
    elif any(x in lower for x in ["food", "restaurant", "eat", "sapda", "saapida", "சாப்பாடு", "சாப்பிட"]):
        answer = f"For {destination_text} ({country_text}), try {profile.get('food', 'local regional dishes and specialties')}. Food-focused areas to explore include {profile.get('places', 'the main city centre and popular local neighbourhoods')}."
    elif any(x in lower for x in ["hotel", "stay", "room", "where to stay"]):
        answer = f"For {destination_text} in {country_text}, choose your stay based on transport access, the areas you want to visit and your ₹{int(budget):,} budget."
    elif any(x in lower for x in ["visa", "passport", "entry", "immigration"]):
        answer = f"Visa and entry rules for {country_text} can change, so they should be checked against the latest official government/consulate guidance before travel."
    elif any(x in lower for x in ["currency", "money", "exchange", "cash", "card"]):
        answer = f"For {country_text}, I can explain the local currency, card/cash usage and typical travel spending. Current exchange rates should be checked live."
    elif any(x in lower for x in ["transport", "metro", "train", "bus", "taxi", "cab", "travel around"]):
        answer = f"For getting around {destination_text} in {country_text}, the best option depends on the city and your itinerary. Public transport is usually best for city sightseeing, while taxis/transfers can help for longer or late-night journeys."
    elif any(x in lower for x in ["safe", "safety", "danger"]):
        answer = f"{destination_text} in {country_text} can be discussed area-by-area for safety, transport and common travel precautions. Current local advisories should be checked before travel."
    elif any(x in lower for x in ["pack", "luggage", "carry"]):
        answer = f"For {destination_text} in {country_text}, {profile.get('pack', 'pack weather-appropriate clothes, documents, chargers, toiletries and comfortable shoes.')}"
    elif any(x in lower for x in ["place", "places", "visit", "where", "attraction", "spot", "see", "enga", "pogalam", "paakalam"]):
        answer = f"For {destination_text} in {country_text}, consider {profile.get('places', 'the main landmarks, local neighbourhoods and cultural attractions')}. The destination is especially known for {profile.get('vibe', 'its local culture and experiences')}."
    elif any(x in lower for x in ["plan", "itinerary", "trip"]):
        answer = f"For a {days}-day {travelers.lower()} trip to {destination_text}, {country_text}, I would build the plan around {profile.get('vibe', 'the destination highlights')}. Key areas include {profile.get('places', 'the main attractions')}, with local food such as {profile.get('food', 'regional specialties')}."
    else:
        answer = f"For {destination_text} in {country_text}, I need the AI service connected to give a full natural-language answer to this question. You can still ask about weather, culture, visa, safety, transport, food, hotels, shopping, nightlife, activities, costs or itinerary."

    return jsonify({"answer": answer})


@app.route("/api/destinations")
def get_destinations():
    return jsonify(DESTINATIONS)


@app.route("/api/search")
def search():
    query = request.args.get("q", "").lower()

    result = [
        d for d in DESTINATIONS
        if query in d["name"].lower()
        or query in d["country"].lower()
        or query in d["region"].lower()
        or any(query in tag.lower() for tag in d["tags"])
    ]

    return jsonify(result)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )