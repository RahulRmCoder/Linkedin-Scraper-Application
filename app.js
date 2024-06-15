import express from 'express';
import bodyParser from 'body-parser';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const port = 3000;

// Get the directory name of the current module file
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.render('index');
});

app.post('/scrape', (req, res) => {
    const linkedinUrl = req.body.linkedin_url;

    // Validate LinkedIn URL format
    const linkedinRegex = /^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$/;
    if (!linkedinRegex.test(linkedinUrl)) {
        return res.send('Invalid LinkedIn URL format.');
    }

    // Run the Python script with the URL
    exec(`py Application/person_scraping.py "${linkedinUrl}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.send('Error occurred while running the script.');
        }
        res.send(`<pre>${stdout}</pre>`);
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
