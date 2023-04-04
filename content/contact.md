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

    form {
        margin-bottom: 2rem;
    }
</style>

<div class="form-container">
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
</div>

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