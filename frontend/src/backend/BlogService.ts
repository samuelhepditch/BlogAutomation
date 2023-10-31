import axios from 'axios';

export class BlogService {
    local: boolean;

    constructor(local: boolean) {
        this.local = local;

        if( local === true){
            axios.defaults.baseURL = 'http://localhost:5000';
        }
    }

    async writeBlog(topic: string, keywords: string): Promise<any> {
        try {
            const response = await axios.post("/write_blog", {topic: topic, keywords: keywords});
            return response;
        } catch (error: unknown) {
            // Handle any errors or rejections from the server here
            console.error("Error writing the blog:", error);
            throw error;
        }
    }
}

