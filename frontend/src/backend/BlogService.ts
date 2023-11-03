import axios from 'axios';
import { BlogStatus } from '../data/BlogStatus';

export class BlogService {
    local: boolean;

    constructor(local: boolean) {
        this.local = local;

        if( local === true){
            axios.defaults.baseURL = 'http://localhost:5000';
        }
    }


    async writeBlog(title: string, keywords: string, blogStatus: BlogStatus): Promise<any> {
        try {
            const response = await axios.post("/write_blog", {title: title, keywords: keywords, status: blogStatus});
            return response;
        } catch (error: unknown) {
            // Handle any errors or rejections from the server here
            console.error("Error writing the blog:", error);
            throw error;
        }
    }
}

