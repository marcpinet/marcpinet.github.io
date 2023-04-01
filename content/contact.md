+++
title = "Contact"
path = "contact"
template = "about.html"
+++

<h1 style="color: #ffaa69">☎️ Contact</h1>

<style>
    h1 {
        font-size: 3rem;
        line-height: 1.5;
    }

    input:focus ~ label, textarea:focus ~ label, input:valid ~ label, textarea:valid ~ label {
        color: #222226;
        top: -5px;
        -webkit-transition: all 0.225s ease;
        transition: all 0.225s ease;
        font-family: 'Roboto Mono', monospace;
    }

    input,
    textarea {
        font-family: 'Roboto Mono', monospace;
        padding: 15px;
        font-size: 1.2rem;
        border: 0;
        width: 97%;
        background-color: #222226;
        color: white;
        border-radius: 4px;
    }

    input:focus,
    textarea:focus { outline: 0; }

    input:focus ~ span,
    textarea:focus ~ span {
        font-family: 'Roboto Mono', monospace;
        width: 100%;
        -webkit-transition: all 0.075s ease;
        transition: all 0.075s ease;
    }

    textarea {
        font-family: 'Roboto Mono', monospace;
        width: 97%;
        min-height: 10em;
        resize: none;
    }

    button {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.2rem;
        padding: 15px;
        border: 0;
        background-color: #ffaa69;
        color: #222226;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 1em;
        transition: all 0.3s ease;
        /*Align to the right*/
        float: right;
    }

    button:hover {
        background-color: #222226;
        color: #ffaa69;
        box-shadow: 0 0 10px #ffaa69;
    }

    .file-container {
        position: relative;
        display: inline-block;
    }

    .file-container input[type="file"] {
        display: none;
    }

    .file-container label {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.2rem;
        padding: 15px;
        border: 0;
        background-color: #ffaa69;
        color: #222226;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .file-container label:hover {
        background-color: #222226;
        color: #ffaa69;
        box-shadow: 0 0 10px #ffaa69;
    }

    .file-name {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.2rem;
        color: white;
        margin-left: 1em;
    }

    .tooltip {
        margin-top: 20px;
        position: absolute;
        z-index: 1;
        visibility: hidden;
        background-color: #222226;
        color: white;
        text-align: center;
        border-radius: 4px;
        padding: 10px;
        font-family: 'Roboto Mono', monospace;
        font-size: 1rem;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s;
        box-sizing: border-box;
    }

    @media (max-width: 480px) {
        .tooltip {
            left: 0;
            right: 0;
            transform: translateX(0);
            width: 100%;
            margin-top: 15px;
            white-space: normal;
            padding-left: 10px; 
            padding-right: 10px;
        }
    }


    .file-container:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
</style>

<form
    action="https://formspree.io/f/mgebnllj"
    method="POST"
    enctype=multipart/form-data
>
    <label>
        Your email:
        <input required type="email" name="email">
    </label>
    <label><br>
        Your message:
        <textarea required name="message"></textarea>
    </label><br><br>
    <div class="file-container"><br>
        <input type="file" name="attachment" id="attachment" onchange="updateFileName()">
        <label for="attachment">Choose File</label>
        <span class="tooltip">⚠️ Refresh the page if you get an error and did not attach anything</span>
        <span class="file-name" id="file-name">No file chosen</span>
    </div><br>
    <button type="submit">Send</button>
</form>

<script>
    function updateFileName() {
        const input = document.getElementById('attachment');
        const fileName = document.getElementById('file-name');
        if (input.files && input.files[0]) {
            fileName.textContent = input.files[0].name;
        } else {
            fileName.textContent = 'No file chosen';
        }
    }
</script>