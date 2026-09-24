import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

export async function get_category(
    state?:string,
    city?:string,
    year?:string,
) {

    const params = new URLSearchParams();

    if(state) params.set('states', state);
    if(city) params.set('city', city);
    if(year) params.set('year',year);

    const response = await fetch(`/api/stats_categories?${params.toString()}`);

    if(!response.ok){
        throw new Error(`Erreur Api : ${response.status}`);
    }

    const data = await response.json();

    return data.map(item => ({
        ...item,
        product_category_name:item.product__product_category_name
            .replace(/_/g, ' ')
            .toLowerCase()
            .replace(/^./, char => char.toUpperCase())
    }))
}


export async function get_delivery(
    state?:string,
    city?:string,
    year?:string,
){
    const params = new URLSearchParams();

    if(state) params.set('states', state);
    if(city) params.set('city', city);
    if(year) params.set('year',year);

    const response = await fetch(`/api/stats_orders?${params.toString()}`);
    const data = await response.json();
    const total = data.reduce(
        (sum, item) => sum + item.count,
        0
    );
    
    return data
        .filter(item => item.count / total >= 0.002)
        .map(item => ({
            ...item,
            order_status: item.order_status
                .replace(/_/g, ' ')
                .toLowerCase()
                .replace(/^./, char => char.toUpperCase()),
            percentage: ((item.count / total) * 100).toFixed(1)
        }));
}


export async function get_payment(
    state?:string,
    city?:string,
    year?:string,
) {

    const params = new URLSearchParams();

    if(state) params.set('states', state);
    if(city) params.set('city', city);
    if(year) params.set('year',year);

    const response = await fetch(`/api/stats_payment_type?${params.toString()}`);
    const data = await response.json();

    // Supprimer les catégories qui représentent moins de 2 %
    const total = data.reduce((sum, item) => sum + item.count, 0);

    return data
        .filter(item => item.count / total >= 0.002)
        .map(item => ({
            ...item,
            payment_type: item.payment_type
                .replace(/_/g, ' ')
                .toLowerCase()
                .replace(/^./, char => char.toUpperCase()),
            percentage: ((item.count / total) * 100).toFixed(1)
        }));
}


export async function get_city(
    state?:string,
    city?:string,
    year?:string,
) {
    const params = new URLSearchParams();

    if(state) params.set('states', state);
    if(city) params.set('city', city);
    if(year) params.set('year',year);

    const response = await fetch(`/api/stats_order_city/?${params.toString()}`);
    const data = await response.json();

    return data;
}


export async function initialize_map() {
    const leaflet = await import('leaflet');
    const L = leaflet.default ?? leaflet;

    (window as any).L = L;

    await import('leaflet.markercluster');

    const map = L.map('map').setView(
        [-23.547, -46.640],
        4
    );

    L.tileLayer(
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            maxZoom: 19,
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }
    ).addTo(map);

    const locationLayer = L.layerGroup().addTo(map);

    return {
        map,
        locationLayer,
        L
    };
}

// Function to get JSON for the map
export async function get_map_data(
    locationLayer: any,
    L: any,
    state?: string,
    city?: string,
    year?: string,
) {
    const params = new URLSearchParams();

    if (state) params.set('states', state);
    if (city) params.set('city', city);
    if (year) params.set('year', year);

    try {
        const response = await fetch(
            `/api/stats_order_locations/?${params.toString()}`
        );

        if (!response.ok) {
            throw new Error(
                `Response status: ${response.status}`
            );
        }
        const result = await response.json();

        const max_number=300;

        result.forEach((location:any) =>{

        })


        locationLayer.clearLayers(); 

        result.forEach((location: any) => {

            const number=Math.min(location.count, max_number)
            const ratio = (number/max_number)
            const red = Math.round((ratio)*255);
            const green = Math.round((1-ratio)*255);

            const circle = L.circle(
                [
                    location.latitude,
                    location.longitude,
                ],
                {
                    color:`rgb(${red},${green},120)`,
                    fillColor:`rgb(${red},${green},120)`,
                    fillOpacity: 0.8,
                    radius: ratio *2500
                }
            ).addTo(locationLayer);

            circle.bindPopup(`
                <strong>Ville :</strong> ${location.city}<br>
                <strong>Commandes :</strong> ${location.count}
            `);
        });

    } catch (error) {
        console.error(error);
    }
}