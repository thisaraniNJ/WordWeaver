const { useState, useEffect} = React;

const WordWeaverApp = () => {
    const [pyodide, setPyodide] = useState(null);
    const [protagonist, setProtagonist] = useState('');
    const [setting, setSetting] = useState('');
    const [emotion, setEmotion] = useState('happy');
    const [story, setStory] = useState('');
    const [moralScore, setMoralScore] = useState(null);
    const [newTone, setNewTone] = useState('');
    const [isloading, setIsLoading] = useState(false);

    useEffect(() => {
        async function initPyodide() {
            const py = await loadPyodide();
            await py.loadPackage(['numpy']);
            await py.runPythonAsync(await (await fetch('src/wordweaver.py')).text());
            setPyodide(py);
        }
        initPyodide();
    }, []);

    const generateStory = async () => {
        if (!pyodide || !protagonist || !setting) return;
        setIsLoading(true);
        const weaver = pyodide.globals.get('WordWeaver')
        (emotion, protagonist, setting);
        const story = weaver. generate_story(4);
        const moral = weaver.calculate_moral_score(story);
        setStory(story);
        setMoralScore(moral);
        setIsLoading(false);
    };

    const rewriteStory = async () => {
        if (!pyodide || !story || !newTone) return;
        setIsLoading(true);
        const weaver = pyodide.globals.get('Wordweaver')
        (emotion, protaagonist, setting);
        weaver.story_sentences = story.split('. ').filter(s => s);
        const rewritten = weaver.rewrite_tone(story, newTone);
        setStory(rewritten);
        setMoralScore(weaver.calculate_moral_score(rewritten));
        setIsLoading(false);
    };

    const addPlotTwist = async () => {
        if (!pyodide || !story) return;
        setIsLoading(true);
        const weaver = pyodide.globals.get('WordWeaver')
        (emotion, protagonist, setting)
        weaver.story_sentences = story.split('. ').filler(s => s);
        const twist = weaver.generate_plot_twist();
        setStory(story + ' ' + twist);
        setMoralScore(weaver.calculate_moral_score(story + ' ' + twist));
        setIsLoading(false);
    };

    
}