// api/read_artifact.js
// Vercel Serverless Function to simulate Aureon's read_Artifact API

export default async function (req, res) {
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { id } = req.query; // Get ID from query parameters

    if (!id) {
        return res.status(400).json({ error: 'Artifact ID is required' });
    }

    try {
        // --- SIMULATION of Aureon's default_api.read_Artifact ---
        // In a real setup, this would call Aureon's deployed REST API.
        // For now, we simulate fetching an artifact based on ID.
        // This is a very basic simulation; a real one would fetch from a database.
        const simulatedArtifacts = [
            { id: 'art_12345678abc', name: 'Initial Brief', content: 'This is a simulated initial briefing document for project "Quantum Leap."', type: 'document', created_date: new Date(Date.now() - 86400000).toISOString() },
            { id: 'art_87654321def', name: 'Code Snippet', content: 'console.log("Hello Aureon!");\n// This is a simulated code artifact.\nfunction greet() {\n  return "Welcome!";\n}', type: 'code', created_date: new Date(Date.now() - 72000000).toISOString() },
            { id: 'art_img123', name: 'Concept Image', content: 'A conceptual image of a coherent energy harvester.', type: 'image', created_date: new Date(Date.now() - 36000000).toISOString() },
            // If the requested ID matches a 'lastCreatedArtifactId' from create_artifact, we can return that.
            // For now, we'll just check against a static list and the passed ID.
        ];

        const foundArtifact = simulatedArtifacts.find(art => art.id === id);

        if (foundArtifact) {
            res.status(200).json([foundArtifact]); // read_Artifact typically returns a list
        } else {
            res.status(404).json({ error: 'Artifact not found.' });
        }
        // --- END SIMULATION ---

    } catch (error) {
        console.error('Error in Vercel read_artifact function:', error);
        res.status(500).json({ error: 'Failed to simulate artifact retrieval.', details: error.message });
    }
}
