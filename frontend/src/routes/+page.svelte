
<div class="content">
    
    <h1>Bienvenue</h1>

    <p class="content_intro">Bienvenue sur la plateforme pour suivre l’avancée de vos opérations. Des dashboards sont mis à votre disposition pour voir l’évolution de votre commerce. De ce fait vous pouvez suivre l’évolution de vos commandes et de vos livraisons ainsi que des catégories les plus populaires et plus encore.</p>

    <div class="space"></div>
    
    <div class="dashboard-content">
        <img src="/placeholder/test.jpg" alt="Graph">
        <div class="dashboard_description">
            <h2>Dashboard</h2>
            <p>Consultez l’évolution de votre commerce.</p><br>
            <button><a href="http://localhost:5173/dashboard">Consulter</a></button>
        </div>
        
    </div>

</div>

<style>
    
    .content{
        padding:2rem;
        display:grid;
    }

    .content h1{
        font-weight: 500;
        font-size: clamp(2rem, 3vw, 2.5rem);
        letter-spacing:-0.02em;
    }
    .content_intro{
        letter-spacing:-0.002em;
        font-weight: 400;
        opacity:0.45;
        text-align:justify;
    }

    .space{
        margin-bottom:4rem;
    }

    a{
        text-decoration:none;
        color:inherit;
    }

    .dashboard_description p{
        letter-spacing:-0.002em;
        font-weight:500;
        opacity:0.55;
    }
    .dashboard-content{
        display:grid;
    }

    button{
        background-color:var(--color-button);
        color:var(--color-white);
        border-radius:0.5rem;
        border:0px;
        display:flex;
        justify-content:center;
        width:100%;
        padding-top:0.8rem;
        padding-bottom:0.8rem;
        font-weight:500;
        font-family:Inter;
    }

    @media (min-width: 1440px) {
        .content {
            padding:1rem 4rem;
        }

        .dashboard-content {
            grid-template-columns: 1fr 1fr;
            grid-template-areas:
            "description image";
            align-items:center;
        }
        .dashboard-content img{
            display:grid;
            grid-area:image;
            align-items:center;
        }
        .dashboard_description{
            grid-area:description;
        }
        .dashboard_description button{
            width:fit-content;
            padding:1.0rem;
        }
    }

</style>