<div class="content">

    <div class=title_page>
        <h1>A propos</h1>
    </div>
    <div class="about_content">
        <div class="stack">
            <h2>Stack Technique utilisé</h2>
            <p>Backend : Django<br>
            Frontend : Svelte<br>
            Base de données : PostgreSQL<br>
            Traitement des données : Python
            </p>
        </div>

        <br>

        <div class="source">
            <h2>Source utilisée</h2>
            <p>Utilisation du dataset d'Olist publié sur Kaggle : <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">Lien du dataset</a><br>
            Illustration graphique placeholder : rawpixel.com</p>
        </div>
        <br>
    </div>
    <p></p>
    <div class="solution">
        <p>Solution développée par Théo Schmitt.</p>
    </div>
</div>

<style>

    .title_page h1{
        font-weight: 500;
        font-size:2.5rem;
        letter-spacing:-0.02em;
    }

    .content{
        padding:2rem;
    }

    .content p{
        letter-spacing:-0.002em;
        font-weight: 400;
        opacity:0.45;
        text-align:justify;
    }


    @media (min-width:1440px){
        .content{
            display: grid;
            padding:1rem 4rem;
        }
        .about_content{
            grid-template-columns:1fr 1fr;
            display:grid;
            grid-template-areas:
            "stack source";
        }
        .stack{
            grid-area:stack;
        }
        .source{
            grid-area:source;
        }
        .solution p{
            text-align:center;
        }

    }
</style>