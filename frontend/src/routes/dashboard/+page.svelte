<script lang="ts">

    let title_graph=$state("");
    function changeTitle(title : string){
        title_graph=title;
    }

</script>

<div class="content">
    <div class=title_page>
        <h1>Dashboard</h1>
    </div>
    <p>Suivez l’évolution de vos commandes et de vos livraisons ainsi que des catégories les plus populaires et plus encore.</p>

    <br>

    <h1 style:display={title_graph ? "block" :"none"}>{title_graph}</h1>
    <div class="graph">
        <img src="/placeholder/test.jpg" alt="Graph">
    </div>
    <div class ="background-filters">
        <div class="filters">
            <button onclick={()=>changeTitle("Catégories")}>Catégories</button>
            <button onclick={()=>changeTitle("Livraisons")}>Livraisons</button>
            <button onclick={()=>changeTitle("Paiement")}>Paiement</button>
        </div>
    </div>
    <br><br>
    
    <div class="graph">
        <img src="/placeholder/test.jpg" alt="Graph">
    </div>
    <div class ="background-filters">
        <div class="filters">
            <button>Villes populaires</button>
        </div>
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
    .filters {
        background: rgba(0, 0, 0, 0.05);
        display:flex;
        justify-content:space-around;
        border-radius: 5% / 90%;
    }
    .filters button{
        background: rgba(233, 124, 124, 0.0);
        border-color:transparent;
        font-weight: 400;
        font-family : Inter;
    }
    @media (min-width:1440px){
        .content{
            padding:1rem 4rem;
        }
        .graph{
            display:flex;
            align-items:center;
            justify-content:center;
        }
        .graph img{
            width:50%;
        }

        .filters{
            padding:0.5% 0.5%;
            width:40%;
        }

        .background-filters{
            display:flex;
            justify-content:center;
        }
        
    }
</style>