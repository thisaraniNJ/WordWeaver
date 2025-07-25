const { useState, useEffect } = React;

const WordWeaverApp = () => {
    const [pyodide, setPyodide] = useState(null);
    const [protagonist, setProtagonist] = useState('');
    const [setting, setSetting] = useState('');
    const [emotion, setEmotion] = useState('happy');
    const [story, setStory] = useState('');
    const [moralScore, setMoralScore] = useState(null);
    const [newTone, setNewTone] = useState('');
    const [isLoading, setIsLoading] = useState(false);

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
        const weaver = pyodide.globals.get('WordWeaver')(emotion, protagonist, setting);
        const story = weaver.generate_story(4);
        const moral = weaver.calculate_moral_score(story);
        setStory(story);
        setMoralScore(moral);
        setIsLoading(false);
    };

    const rewriteStory = async () => {
        if (!pyodide || !story || !newTone) return;
        setIsLoading(true);
        const weaver = pyodide.globals.get('WordWeaver')(emotion, protagonist, setting);
        weaver.story_sentences = story.split('. ').filter(s => s);
        const rewritten = weaver.rewrite_tone(story, newTone);
        setStory(rewritten);
        setMoralScore(weaver.calculate_moral_score(rewritten));
        setIsLoading(false);
    };

    const addPlotTwist = async () => {
        if (!pyodide || !story) return;
        setIsLoading(true);
        const weaver = pyodide.globals.get('WordWeaver')(emotion, protagonist, setting);
        weaver.story_sentences = story.split('. ').filter(s => s);
        const twist = weaver.generate_plot_twist();
        setStory(story + ' ' + twist);
        setMoralScore(weaver.calculate_moral_score(story + ' ' + twist));
        setIsLoading(false);
    };

    return (
        <div className="max-w-2xl w-full bg-white/90 backdrop-blur-lg rounded-2xl p-8 glow">
            <h1 className="text-3xl font-bold text-center gradient-text mb-6">WordWeaver</h1>
            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Protagonist</label>
                    <input
                        type="text"
                        value={protagonist}
                        onChange={(e) => setProtagonist(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                        placeholder="e.g., Dr. Raven"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Setting</label>
                    <input
                        type="text"
                        value={setting}
                        onChange={(e) => setSetting(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                        placeholder="e.g., Abandoned research facility"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Emotion</label>
                    <select
                        value={emotion}
                        onChange={(e) => setEmotion(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                    >
                        <option value="happy">Happy</option>
                        <option value="sad">Sad</option>
                        <option value="fearful">Fearful</option>
                        <option value="suspense">Suspense</option>
                        <option value="comedy">Comedy</option>
                    </select>
                </div>
                <button
                    onClick={generateStory}
                    disabled={isLoading || !protagonist || !setting}
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-md hover:from-purple-700 hover:to-pink-700 disabled:opacity-50"
                >
                    {isLoading ? 'Generating...' : 'Generate Story'}
                </button>
                {story && (
                    <div className="mt-6 p-4 bg-gray-50 rounded-md">
                        <h2 className="text-lg font-semibold text-gray-800">Story</h2>
                        <p className="text-gray-600 mt-2">{story}</p>
                        <p className="text-sm text-gray-500 mt-2">Moral Score: {moralScore}</p>
                        <div className="mt-4 flex space-x-2">
                            <select
                                value={newTone}
                                onChange={(e) => setNewTone(e.target.value)}
                                className="rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                            >
                                <option value="">Change Tone...</option>
                                <option value="happy">Happy</option>
                                <option value="sad">Sad</option>
                                <option value="fearful">Fearful</option>
                                <option value="suspense">Suspense</option>
                                <option value="comedy">Comedy</option>
                            </select>
                            <button
                                onClick={rewriteStory}
                                disabled={isLoading || !newTone}
                                className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50"
                            >
                                Rewrite Tone
                            </button>
                            <button
                                onClick={addPlotTwist}
                                disabled={isLoading}
                                className="bg-pink-600 text-white px-4 py-2 rounded-md hover:bg-pink-700 disabled:opacity-50"
                            >
                                Add Plot Twist
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<WordWeaverApp />);