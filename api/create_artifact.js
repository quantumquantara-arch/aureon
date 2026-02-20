// api/create_artifact.js
// Vercel Serverless Function to simulate Aureon's create_Artifact API

export default async function (req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { name, content, type } = req.body;

    if (!name || !content) {
        return res.status(400).json({ error: 'Name and content are required' });
    }

    try {
        // --- SIMULATION of Aureon's default_api.create_Artifact ---
        // In a real setup, this would call Aureon's deployed REST API.
        // For now, we generate a realistic-looking response.
        const simulatedArtifact = { 
            id: 'art_' + Date.now().toString().slice(-8) + Math.random().toString(36).substring(2, 6), // Unique enough ID
            name: name, 
            content: content, 
            type: type || 'text',
            created_date: new Date().toISOString(),
            visibility: 'private',
            task_id: null // Can be expanded later
        };
        // --- END SIMULATION ---

        res.status(200).json(simulatedArtifact);
    } catch (error) {
        console.error('Error in Vercel create_artifact function:', error);
        res.status(500).json({ error: 'Failed to simulate artifact creation.', details: error.message });
    }
}
