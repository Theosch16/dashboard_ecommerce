<footer class="footers">
    <hr>
    <div class="line-footer">
        <h4>Théo SCHMITT - @2026</h4>
        <p>Olist Kaggle Dataset</p>
    </div>
</footer>

<style>
    .footers{
        width:100%;
    }
    
    .footers hr{
        border:none;
        height:1px;
        color: var(--color-text);
        background-color:var(--color-background);
    }

    .footers p{
        text-align:center;
        font-weight:300;
        opacity:0.55;
    }
    .line-footer{
        padding: 1rem;
        display:grid;
        grid-template-columns:1fr 1fr;
        grid-template-areas:"credit source";
        align-items:center;
    }
    .line-footer {
        justify-content:center;
        align-items:center;
        grid-area:credit;
    }
    .line-footer > :first-child {
        grid-area: credit;
        margin: 0;
        text-align: center;
    }

    .line-footer > :last-child {
        grid-area: source;
        margin: 0;
        text-align: center;
    }
</style>

